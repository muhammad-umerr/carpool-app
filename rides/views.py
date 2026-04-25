from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import F
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import JoinRideForm, RideCreateForm, SignUpForm
from .models import Ride, RideParticipant


def landing_view(request):
	if request.user.is_authenticated:
		return redirect("rides:home")
	return render(request, "rides/landing.html")


def signup_view(request):
	if request.user.is_authenticated:
		return redirect("rides:home")

	if request.method == "POST":
		form = SignUpForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Welcome! Your account has been created.")
			return redirect("rides:home")
	else:
		form = SignUpForm()

	return render(request, "registration/signup.html", {"form": form})


@login_required
def home_view(request):
	available_rides = (
		Ride.objects.select_related("driver")
		.prefetch_related("pickup_stops")
		.filter(status__in=[Ride.Status.OPEN, Ride.Status.ACTIVE], seats_available__gt=0)
		.exclude(driver=request.user)
		.filter(departure_time__gte=timezone.now())
	)
	joined_ids = set(
		RideParticipant.objects.filter(user=request.user).values_list("ride_id", flat=True)
	)

	join_form = JoinRideForm()
	return render(
		request,
		"rides/home.html",
		{
			"available_rides": available_rides,
			"join_form": join_form,
			"joined_ids": joined_ids,
		},
	)


@login_required
def create_ride_view(request):
	if request.method == "POST":
		create_form = RideCreateForm(request.POST)
		if create_form.is_valid():
			create_form.save(driver=request.user)
			messages.success(request, "Ride added successfully.")
			return redirect("rides:home")
	else:
		create_form = RideCreateForm()

	return render(request, "rides/create_ride.html", {"create_form": create_form})


@login_required
@transaction.atomic
def join_ride_view(request, ride_id):
	if request.method != "POST":
		return redirect("rides:home")

	ride = get_object_or_404(Ride.objects.select_for_update(), pk=ride_id)
	if ride.driver_id == request.user.id:
		messages.error(request, "You cannot join your own ride.")
		return redirect("rides:home")

	if ride.status == Ride.Status.FINALIZED:
		messages.error(request, "This ride is already finalized.")
		return redirect("rides:home")

	if RideParticipant.objects.filter(ride=ride, user=request.user).exists():
		messages.info(request, "You already joined this ride.")
		return redirect("rides:home")

	form = JoinRideForm(request.POST)
	if not form.is_valid():
		messages.error(request, "Please provide contact number and pickup location.")
		return redirect("rides:home")

	if ride.seats_available <= 0:
		messages.error(request, "No seats left for this ride.")
		return redirect("rides:home")

	RideParticipant.objects.create(
		ride=ride,
		user=request.user,
		contact_number=form.cleaned_data["contact_number"],
		pickup_location=form.cleaned_data["pickup_location"],
	)

	Ride.objects.filter(pk=ride.pk, seats_available__gt=0).update(
		seats_available=F("seats_available") - 1,
		status=Ride.Status.ACTIVE,
	)
	messages.success(request, "You have joined the ride.")
	return redirect("rides:current_rides")


@login_required
def current_rides_view(request):
	driving_rides = (
		Ride.objects.filter(driver=request.user, status__in=[Ride.Status.OPEN, Ride.Status.ACTIVE])
		.prefetch_related("participants__user", "pickup_stops")
		.order_by("departure_time")
	)
	passenger_entries = (
		RideParticipant.objects.select_related("ride", "ride__driver")
		.prefetch_related("ride__pickup_stops")
		.filter(user=request.user, ride__status__in=[Ride.Status.OPEN, Ride.Status.ACTIVE])
		.order_by("ride__departure_time")
	)
	return render(
		request,
		"rides/current_rides.html",
		{"driving_rides": driving_rides, "passenger_entries": passenger_entries},
	)


@login_required
@transaction.atomic
def finalize_ride_view(request, ride_id):
	if request.method != "POST":
		return redirect("rides:current_rides")

	ride = get_object_or_404(Ride.objects.select_for_update(), pk=ride_id, driver=request.user)
	if ride.status == Ride.Status.FINALIZED:
		messages.info(request, "Ride already finalized.")
		return redirect("rides:current_rides")

	ride.finalize()
	messages.success(request, "Ride finalized. Passengers can now simulate payment.")
	return redirect("rides:recent_rides")


@login_required
@transaction.atomic
def simulate_payment_view(request, ride_id):
	if request.method != "POST":
		return redirect("rides:recent_rides")

	participant = get_object_or_404(
		RideParticipant.objects.select_related("ride"),
		ride_id=ride_id,
		user=request.user,
	)

	if participant.ride.status != Ride.Status.FINALIZED:
		messages.error(request, "Payment is available only after ride finalization.")
		return redirect("rides:current_rides")

	if participant.payment_status == RideParticipant.PaymentStatus.PAID:
		messages.info(request, "Payment already simulated.")
		return redirect("rides:recent_rides")

	participant.payment_status = RideParticipant.PaymentStatus.PAID
	participant.paid_at = timezone.now()
	participant.save(update_fields=["payment_status", "paid_at"])
	messages.success(request, "Payment simulated successfully.")
	return redirect("rides:recent_rides")


@login_required
def recent_rides_view(request):
	completed_as_driver = (
		Ride.objects.filter(driver=request.user, status=Ride.Status.FINALIZED)
		.prefetch_related("participants__user", "pickup_stops")
		.order_by("-finalized_at")
	)
	completed_as_passenger = (
		RideParticipant.objects.select_related("ride", "ride__driver")
		.prefetch_related("ride__pickup_stops")
		.filter(user=request.user, ride__status=Ride.Status.FINALIZED)
		.order_by("-ride__finalized_at")
	)

	pending_payment_count = completed_as_passenger.filter(
		payment_status=RideParticipant.PaymentStatus.PENDING
	).count()

	return render(
		request,
		"rides/recent_rides.html",
		{
			"completed_as_driver": completed_as_driver,
			"completed_as_passenger": completed_as_passenger,
			"pending_payment_count": pending_payment_count,
		},
	)

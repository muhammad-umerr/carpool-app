from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Ride(models.Model):
	class Status(models.TextChoices):
		OPEN = "OPEN", "Open"
		ACTIVE = "ACTIVE", "Active"
		FINALIZED = "FINALIZED", "Finalized"

	driver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="driven_rides")
	origin = models.CharField(max_length=120)
	destination = models.CharField(max_length=120)
	departure_time = models.DateTimeField()
	pickup_point = models.CharField(max_length=120)
	seats_total = models.PositiveIntegerField(default=1)
	seats_available = models.PositiveIntegerField(default=1)
	fare_per_seat = models.DecimalField(max_digits=7, decimal_places=2)
	notes = models.TextField(blank=True)
	status = models.CharField(max_length=16, choices=Status.choices, default=Status.OPEN)
	finalized_at = models.DateTimeField(null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ["departure_time", "-created_at"]

	def __str__(self):
		return f"{self.origin} to {self.destination} ({self.departure_time:%Y-%m-%d %H:%M})"

	def finalize(self):
		self.status = self.Status.FINALIZED
		self.finalized_at = timezone.now()
		self.save(update_fields=["status", "finalized_at", "updated_at"])

	@property
	def pickup_locations(self):
		stops = list(self.pickup_stops.order_by("stop_order").values_list("location", flat=True))
		if stops:
			return stops
		return [self.pickup_point]


class RidePickupStop(models.Model):
	ride = models.ForeignKey(Ride, on_delete=models.CASCADE, related_name="pickup_stops")
	location = models.CharField(max_length=120)
	stop_order = models.PositiveIntegerField(default=1)

	class Meta:
		ordering = ["stop_order", "id"]
		unique_together = ("ride", "stop_order")

	def __str__(self):
		return f"{self.ride_id} stop {self.stop_order}: {self.location}"


class RideParticipant(models.Model):
	class PaymentStatus(models.TextChoices):
		PENDING = "PENDING", "Pending"
		PAID = "PAID", "Paid"

	ride = models.ForeignKey(Ride, on_delete=models.CASCADE, related_name="participants")
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="joined_rides")
	contact_number = models.CharField(max_length=20)
	pickup_location = models.CharField(max_length=120)
	payment_status = models.CharField(
		max_length=12,
		choices=PaymentStatus.choices,
		default=PaymentStatus.PENDING,
	)
	paid_at = models.DateTimeField(null=True, blank=True)
	joined_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		unique_together = ("ride", "user")
		ordering = ["joined_at"]

	def __str__(self):
		return f"{self.user.username} in {self.ride}"

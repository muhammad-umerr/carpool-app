from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User

from .models import Ride, RideParticipant, RidePickupStop


class RideFlowTests(TestCase):
	def setUp(self):
		self.driver = User.objects.create_user(username="driver", password="pass12345")
		self.passenger = User.objects.create_user(username="passenger", password="pass12345")
		self.ride = Ride.objects.create(
			driver=self.driver,
			origin="Campus Gate",
			destination="City Center",
			departure_time=timezone.now() + timedelta(hours=2),
			pickup_point="Main Gate",
			seats_total=2,
			seats_available=2,
			fare_per_seat="3.50",
		)

	def test_passenger_can_join_ride(self):
		self.client.login(username="passenger", password="pass12345")
		response = self.client.post(
			reverse("rides:join_ride", args=[self.ride.id]),
			{"contact_number": "12345", "pickup_location": "Library Stop"},
			follow=True,
		)

		self.assertEqual(response.status_code, 200)
		self.ride.refresh_from_db()
		self.assertEqual(self.ride.seats_available, 1)
		self.assertEqual(self.ride.status, Ride.Status.ACTIVE)
		self.assertTrue(
			RideParticipant.objects.filter(ride=self.ride, user=self.passenger).exists()
		)

	def test_driver_can_finalize_ride(self):
		self.client.login(username="driver", password="pass12345")
		response = self.client.post(reverse("rides:finalize_ride", args=[self.ride.id]), follow=True)
		self.assertEqual(response.status_code, 200)
		self.ride.refresh_from_db()
		self.assertEqual(self.ride.status, Ride.Status.FINALIZED)
		self.assertIsNotNone(self.ride.finalized_at)

	def test_passenger_can_simulate_payment_after_finalization(self):
		participant = RideParticipant.objects.create(
			ride=self.ride,
			user=self.passenger,
			contact_number="12345",
			pickup_location="Library Stop",
		)
		self.ride.finalize()

		self.client.login(username="passenger", password="pass12345")
		response = self.client.post(reverse("rides:simulate_payment", args=[self.ride.id]), follow=True)
		self.assertEqual(response.status_code, 200)

		participant.refresh_from_db()
		self.assertEqual(participant.payment_status, RideParticipant.PaymentStatus.PAID)
		self.assertIsNotNone(participant.paid_at)

	def test_driver_can_add_multiple_pickup_stops(self):
		self.client.login(username="driver", password="pass12345")
		response = self.client.post(
			reverse("rides:create_ride"),
			{
				"origin": "Block A",
				"destination": "Science Park",
				"departure_time": (timezone.now() + timedelta(hours=4)).strftime("%Y-%m-%dT%H:%M"),
				"pickup_point": "Main Gate",
				"pickup_stops_text": "Library Stop\nHostel Gate, Cafeteria",
				"seats_total": 3,
				"fare_per_seat": "4.50",
				"notes": "Evening ride",
			},
			follow=True,
		)

		self.assertEqual(response.status_code, 200)
		ride = Ride.objects.get(origin="Block A", destination="Science Park")
		stops = list(
			RidePickupStop.objects.filter(ride=ride).order_by("stop_order").values_list("location", flat=True)
		)
		self.assertEqual(stops, ["Main Gate", "Library Stop", "Hostel Gate", "Cafeteria"])

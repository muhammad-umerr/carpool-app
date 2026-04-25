from django.contrib import admin

from .models import Ride, RideParticipant, RidePickupStop


@admin.register(Ride)
class RideAdmin(admin.ModelAdmin):
	list_display = (
		"id",
		"driver",
		"origin",
		"destination",
		"departure_time",
		"status",
		"seats_available",
	)
	list_filter = ("status", "departure_time")
	search_fields = ("origin", "destination", "driver__username", "driver__email")


@admin.register(RideParticipant)
class RideParticipantAdmin(admin.ModelAdmin):
	list_display = ("id", "ride", "user", "payment_status", "joined_at", "paid_at")
	list_filter = ("payment_status", "joined_at")
	search_fields = ("user__username", "user__email", "ride__origin", "ride__destination")


@admin.register(RidePickupStop)
class RidePickupStopAdmin(admin.ModelAdmin):
	list_display = ("id", "ride", "stop_order", "location")
	list_filter = ("stop_order",)
	search_fields = ("ride__origin", "ride__destination", "location")

# Register your models here.

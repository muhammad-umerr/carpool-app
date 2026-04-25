from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils import timezone

from .models import Ride, RidePickupStop


class StyledAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Username",
                "autocomplete": "username",
            }
        )
        self.fields["password"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Password",
                "autocomplete": "current-password",
            }
        )


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            existing_class = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"{existing_class} form-control".strip()


class RideCreateForm(forms.ModelForm):
    pickup_stops_text = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"rows": 3}),
        help_text="Add one stop per line, or separate by commas.",
        label="Additional pickup stops",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            existing_class = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"{existing_class} form-control".strip()

    class Meta:
        model = Ride
        fields = [
            "origin",
            "destination",
            "departure_time",
            "pickup_point",
            "pickup_stops_text",
            "seats_total",
            "fare_per_seat",
            "notes",
        ]
        widgets = {
            "departure_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }

    def clean_pickup_stops_text(self):
        raw_value = self.cleaned_data.get("pickup_stops_text", "")
        tokens = [item.strip() for item in raw_value.replace("\r", "").replace(",", "\n").split("\n")]
        stops = [item for item in tokens if item]
        return stops

    def clean_departure_time(self):
        departure_time = self.cleaned_data["departure_time"]
        if departure_time <= timezone.now():
            raise forms.ValidationError("Departure time must be in the future.")
        return departure_time

    def save(self, commit=True, driver=None):
        ride = super().save(commit=False)
        if driver is not None:
            ride.driver = driver
        ride.seats_available = ride.seats_total
        if commit:
            ride.save()

            stops = [ride.pickup_point]
            for stop in self.cleaned_data.get("pickup_stops_text", []):
                if stop not in stops:
                    stops.append(stop)

            for index, stop in enumerate(stops, start=1):
                RidePickupStop.objects.create(
                    ride=ride,
                    location=stop,
                    stop_order=index,
                )
        return ride


class JoinRideForm(forms.Form):
    contact_number = forms.CharField(max_length=20)
    pickup_location = forms.CharField(max_length=120)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            existing_class = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"{existing_class} form-control".strip()

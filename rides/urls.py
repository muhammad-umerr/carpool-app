from django.urls import path

from . import views

app_name = "rides"

urlpatterns = [
    path("", views.landing_view, name="landing"),
    path("home/", views.home_view, name="home"),
    path("rides/create/", views.create_ride_view, name="create_ride"),
    path("signup/", views.signup_view, name="signup"),
    path("rides/current/", views.current_rides_view, name="current_rides"),
    path("rides/recent/", views.recent_rides_view, name="recent_rides"),
    path("rides/<int:ride_id>/join/", views.join_ride_view, name="join_ride"),
    path("rides/<int:ride_id>/finalize/", views.finalize_ride_view, name="finalize_ride"),
    path("rides/<int:ride_id>/pay/", views.simulate_payment_view, name="simulate_payment"),
]

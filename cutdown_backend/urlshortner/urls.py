

from django.urls import re_path

from urlshortner.views import HealthCheckView

urlpatterns = [
    re_path(
        r"^status$",
        HealthCheckView.as_view(),
        name="health_check",
    )
    ]
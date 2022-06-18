from django.urls import re_path

from urlshortner.views import HealthCheckView, RedirectURLView, ShortenURLView

urlpatterns = [
    re_path(
        r"^api/status$",
        HealthCheckView.as_view(),
        name="health_check",
    ),
    re_path(
        r"^shorten_url/$",
        ShortenURLView.as_view(),
        name="shorten_url",
    ),
    re_path(
        r"^(?P<shorten_key>[^/.]+)$",
        RedirectURLView.as_view(),
        name="redirect",
    ),
]

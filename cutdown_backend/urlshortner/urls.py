from django.urls import re_path

from urlshortner.views import HealthCheckView, RedirectURLView, ShortenURLView, FreeShortenURLView

urlpatterns = [
    re_path(
        r"^health$",
        HealthCheckView.as_view(),
        name="health_check",
    ),
    re_path(
        r"^shorten_url/free$",
        FreeShortenURLView.as_view(),
        name="free_shorten_url",
    ),
    re_path(
        r"^shorten_url$",
        ShortenURLView.as_view(),
        name="shorten_url",
    ),
    re_path(
        r"^(?P<cutdown_url>[^/.]+)$",
        RedirectURLView.as_view(),
        name="redirect",
    ),
]

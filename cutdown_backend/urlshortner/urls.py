from django.urls import re_path

# from cutdown_backend.urlshortner.models import CutDownUrl

from urlshortner.views import HealthCheckView

urlpatterns = [
    re_path(
        r"^api/status$",
        HealthCheckView.as_view(),
        name="health_check",
    ),
    # re_path(
    #     r"^create_coutdown_url$",
    #     CutDownUrlView.as_view(),
    #     name="health_check",
    # )
]

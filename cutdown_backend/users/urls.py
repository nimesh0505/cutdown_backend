from rest_framework.routers import DefaultRouter

from users.views import SignupView

router = DefaultRouter()
router.register(f"", SignupView, basename="signup")

urlpatterns = [] + router.urls

from django.urls import path
from rest_framework.routers import DefaultRouter

from users import views

router = DefaultRouter()
router.register(f"signup", views.SignupView, basename="signup")
router.register(f"signin", views.SignInView, basename="signin")

urlpatterns = [] + router.urls

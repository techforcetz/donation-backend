from django.urls import path
from .views import Register,Login
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
urlpatterns = [
    # token
    path("api/token/", TokenObtainPairView.as_view(), name=""),
    path("api/token/refresh/", TokenRefreshView.as_view(), name=""),
    
    path("register",Register.as_view(),name="test"),
    path("login",Login.as_view(),name="login")
]

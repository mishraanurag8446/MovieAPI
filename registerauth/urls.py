from django.urls import path
from .views import UserRegistrationView, CustomTokenObtainPairView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token-obtain-pair'),
    # other endpoints with authentication required
    # ...
]

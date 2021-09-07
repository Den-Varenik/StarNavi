from rest_framework_simplejwt.views import (TokenRefreshView, TokenObtainPairView)
from django.urls import path

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

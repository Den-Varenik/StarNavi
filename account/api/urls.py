from rest_framework_simplejwt.views import (TokenRefreshView, TokenObtainPairView)
from django.urls import path

from account.api.views import registration_view

urlpatterns = [
    path('register/', registration_view, name="register"),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

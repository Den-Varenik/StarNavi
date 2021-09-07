from django.urls import path, include
from rest_framework.routers import DefaultRouter

from posts.api.views import PostVS

router = DefaultRouter()
router.register('z', PostVS, basename='post')

urlpatterns = [
    path('', include(router.urls)),
]

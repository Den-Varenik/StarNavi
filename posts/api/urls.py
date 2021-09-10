from django.urls import path, include
from rest_framework.routers import DefaultRouter

from posts.api.views import PostVS, LikeList, LikeDelete, LikeAnalytics

router = DefaultRouter()
router.register('', PostVS, basename='post')

urlpatterns = [
    path('', include(router.urls)),
    path('<int:pk>/likes/', LikeList.as_view(), name="like-list"),
    path('<int:pk>/likes/analytics/', LikeAnalytics.as_view(), name="like-analytics"),
    path('likes/<int:pk>/', LikeDelete.as_view(), name="like-delete"),
]

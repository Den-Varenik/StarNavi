from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.validators import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response

from django.db.models import Count
from django.db.models.functions import TruncDay
from datetime import datetime

from posts.models import Post, Like
from posts.api.serializers import PostSerializer, LikeSerializer, LikeAnalyticSerializer
from posts.api.permissions import IsAuthorOrReadOnly, IsLikerOrReadOnly


class PostVS(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        author = self.request.user
        serializer.save(author=author)


class LikeList(generics.ListCreateAPIView):
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        pk = self.kwargs["pk"]
        return Like.objects.filter(like_post=pk)

    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        like_post = Post.objects.get(pk=pk)

        like_user = self.request.user
        like_queryset = Like.objects.filter(like_post=like_post, like_user=like_user)

        if like_queryset.exists():
            raise ValidationError("You have already liked this post!")

        serializer.save(like_post=like_post, like_user=like_user)


class LikeDelete(generics.DestroyAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsLikerOrReadOnly]


class LikeAnalytics(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, pk):
        post = Post.objects.get(pk=pk)

        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')

        try:
            datetime.strptime(date_from, '%Y-%m-%d')
            datetime.strptime(date_to, '%Y-%m-%d')
        except ValueError:
            return Response({"Error": "Incorrect data format, should be YYYY-MM-DD"}, status=status.HTTP_400_BAD_REQUEST)
        except TypeError:
            return Response({"Error": "No query params 'date_from' and 'date_to'!"}, status=status.HTTP_400_BAD_REQUEST)

        analytics = post.likes.filter(created__range=["2021-01-01", "2021-09-11"]) \
            .annotate(date=TruncDay("created")).values("date") \
            .annotate(amount=Count('id')).order_by("-date")

        serializer = LikeAnalyticSerializer(analytics, many=True)

        return Response(serializer.data)

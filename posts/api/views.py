from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.validators import ValidationError

from posts.models import Post, Like
from posts.api.serializers import PostSerializer, LikeSerializer
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

from rest_framework import viewsets

from posts.models import Post
from posts.api.serializers import PostSerializer
from posts.api.permissions import IsAuthorOrReadOnly


class PostVS(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        author = self.request.user
        serializer.save(author=author)

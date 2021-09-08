from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from posts.api.serializers import PostSerializer
from posts.models import Post


class PostVS(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        author = self.request.user
        serializer.save(author=author)

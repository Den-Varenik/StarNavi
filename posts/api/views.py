from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from posts.api.serializers import PostSerializer
from posts.models import Post


class PostVS(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

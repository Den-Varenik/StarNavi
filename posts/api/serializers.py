from rest_framework import serializers
from posts.models import Post


class PostSerializer(serializers.ModelSerializer):
    post_user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Post
        fields = "__all__"

    def save(self):
        title = self.validated_data["title"]
        description = self.validated_data["description"]
        active = self.validated_data["active"]
        user = self.context["request"].user
        post = Post(title=title, description=description, active=active, post_user=user)
        post.save()
        return post

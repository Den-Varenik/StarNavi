from rest_framework import serializers
from posts.models import Post, Like


class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Post
        fields = "__all__"


class LikeSerializer(serializers.ModelSerializer):
    like_user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Like
        exclude = ("like_post",)

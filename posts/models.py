from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    text = models.TextField()
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.title)


class Like(models.Model):
    like_user = models.ForeignKey(User, on_delete=models.CASCADE)
    like_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.like_post.title} - {self.like_post.likes.all().count()}'

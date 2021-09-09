from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from posts import models


class PostTestCase(APITestCase):

    def setUp(self) -> None:
        self.user1 = User.objects.create_user(username="test",
                                              email="test@example.com",
                                              password="Test@123")
        self.refresh1 = RefreshToken.for_user(self.user1)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh1.access_token}')

        self.user2 = User.objects.create_user(username="test2",
                                        email="test2@example.com",
                                        password="Test@123")
        self.refresh2 = RefreshToken.for_user(self.user2)

        self.post = models.Post.objects.create(author=self.user1,
                                               title="Test Post",
                                               text="Lorem ipsum...",
                                               active=True)

    def test_post_list(self):
        response = self.client.get(reverse('post-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_create(self):
        data = {
            "author": self.user1,
            "title": "Test Create Post",
            "text": "Lorem ipsum...",
            "active": True
        }

        response = self.client.post(reverse('post-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.Post.objects.all().count(), 2)

    def test_post_update(self):
        data = {
            "title": "Test Update Post",
            "text": "Lorem ipsum...",
            "active": True
        }

        response = self.client.put(reverse('post-detail', args=(self.post.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(models.Post.objects.get(pk=self.post.id).title, "Test Update Post")

    def test_post_delete(self):
        response = self.client.delete(reverse('post-detail', args=(self.post.id,)))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(models.Post.objects.all().count(), 0)

    def test_post_list_unauth(self):
        self.client.force_authenticate(user=None)

        response = self.client.get(reverse('post-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_update_unauth(self):
        self.client.force_authenticate(user=None)

        data = {
            "title": "Test Un Auth Update Post",
            "text": "Lorem ipsum...",
            "active": True
        }

        response = self.client.put(reverse('post-detail', args=(self.post.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_delete_unauth(self):
        self.client.force_authenticate(user=None)

        response = self.client.delete(reverse('post-detail', args=(self.post.id,)))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_update_noauthor(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh2.access_token}')

        data = {
            "title": "Test No Author Update Post",
            "text": "Lorem ipsum...",
            "active": True
        }

        response = self.client.put(reverse('post-detail', args=(self.post.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_delete_noauthor(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh2.access_token}')

        response = self.client.delete(reverse('post-detail', args=(self.post.id,)))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class LikeTestCase(APITestCase):

    def setUp(self) -> None:
        self.user1 = User.objects.create_user(username="test",
                                              email="test@example.com",
                                              password="Test@123")
        self.refresh1 = RefreshToken.for_user(self.user1)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh1.access_token}')

        self.user2 = User.objects.create_user(username="test2",
                                              email="test2@example.com",
                                              password="Test@123")
        self.refresh2 = RefreshToken.for_user(self.user2)

        self.post = models.Post.objects.create(author=self.user1,
                                               title="Test Post",
                                               text="Lorem ipsum...",
                                               active=True)

        self.like = models.Like.objects.create(like_user=self.user1,
                                               like_post=self.post)

    def test_like_list(self):
        response = self.client.get(reverse('like-list', args=(self.post.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_like_create(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh2.access_token}')

        response = self.client.post(reverse('like-list', args=(self.post.id,)))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_like_double_create(self):
        response = self.client.post(reverse('like-list', args=(self.post.id,)))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_like_delete(self):
        response = self.client.delete(reverse('like-delete', args=(self.like.id,)))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_like_delete_no_liked_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.refresh2.access_token}")

        response = self.client.delete(reverse('like-delete', args=(self.like.id,)))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

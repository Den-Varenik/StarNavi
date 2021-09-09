from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase


class RegisterTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(username="test",
                                             email="test@example.com",
                                             password="Test@123")

    def test_register(self):
        data = dict(username='testcase', email='testcase@example.com', password='TestCase@123')

        data["password2"] = "TestCase@1234"
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data["email"] = "test@example.com"
        data["password2"] = "TestCase@123"
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data["email"] = "testcase@example.com"
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class LoginLogoutTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(username="test",
                                             email="test@example.com",
                                             password="Test@123")

    def test_login(self):
        data = dict(username="test")

        data["password"] = "Test@1234"
        response = self.client.post(reverse('token_obtain_pair'), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        data["password"] = "Test@123"
        response = self.client.post(reverse('token_obtain_pair'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

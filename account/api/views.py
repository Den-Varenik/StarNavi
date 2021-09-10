from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAdminUser

from account.api.serializers import RegistrationSerializer


@api_view(["POST"])
def registration_view(request):

    if request.method == "POST":
        serializer = RegistrationSerializer(data=request.data)

        data = {}

        if serializer.is_valid():
            account = serializer.save()

            data["response"] = "Registration Successful!"
            data["username"] = account.username
            data["email"] = account.email

            refresh = RefreshToken.for_user(user=account)
            data["token"] = {
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            }
        else:
            data = serializer.errors

        return Response(data, status=status.HTTP_201_CREATED)


@api_view(["GET"])
@permission_classes([IsAdminUser])
def activity_view(request, pk):
    last_login = User.objects.get(pk=pk).last_login
    data = {
        "last_login": last_login,
        "last_request": ""
    }
    return Response(data)

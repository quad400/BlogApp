from rest_framework import generics,permissions,authentication,mixins
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import HTTP_201_CREATED,HTTP_200_OK
from django.conf import settings

from .serializers import RegisterSerializer, ProfileSerializer

from core.utils import handle_errors
from core.services import UserAuthService
from core.authentication import TokenAuthentication
from .models import User

auth_service = UserAuthService()

# User = settings.AUTH_USER_MODEL

class SignUpView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    @handle_errors() 
    def post(self, request:Request):
        return Response({
            "data": auth_service.register_user(
                username=request.data.get("username"),
                email=request.data.get("email"),
                password=request.data.get("password"),
                confirm_password=request.data.get("confirm_password")
            )
        },
            status=HTTP_201_CREATED,
        )


class LoginView(APIView):
    permission_classes = []

    @handle_errors()
    def post(self, request: Request):
        username = request.data.get("username")
        password = request.data.get("password")

        return Response(
            {
                "data": auth_service.login_user(username=username, password=password)
            },
            status=HTTP_200_OK
        )

class ProfileUpdateView(generics.UpdateAPIView):
    serializer_class = ProfileSerializer
    queryset = User
    lookup_field='pk'
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [
        authentication.SessionAuthentication,
        TokenAuthentication
    ]

    def perform_update(self,serializer):
        instance = serializer.save()
        if not User.objects.none():
            instance.profile_pic = serializer.validated_data.pop("profile_pic")
        return instance


class ProfileDetailView(generics.RetrieveAPIView):
    serializer_class = ProfileSerializer
    queryset = User
    lookup_field='pk'
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [
        authentication.SessionAuthentication,
        TokenAuthentication
    ]

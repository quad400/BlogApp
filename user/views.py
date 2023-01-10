from rest_framework import generics,permissions,authentication,mixins
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import HTTP_201_CREATED,HTTP_200_OK,HTTP_400_BAD_REQUEST,HTTP_202_ACCEPTED


from .serializers import RegisterSerializer,UserSerializer,LoginSerializer
from core.utils import handle_errors
from core.services import UserAuthService
from core.authentication import TokenAuthentication
from core.permissions import IsOwnerOrReadOnly
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
            )
        },
            status=HTTP_201_CREATED,
        )


class LoginView(APIView):
    permission_classes = []
    serializer_class=LoginSerializer

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


class UserUpdateView(generics.RetrieveAPIView,generics.UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User
    lookup_field='pk'
    permission_classes = [IsOwnerOrReadOnly]
    authentication_classes = [
        authentication.SessionAuthentication,
        TokenAuthentication
    ]

    def perform_update(self,serializer):
        instance = serializer.save()
        if not User.objects.none():
            instance.first_name = serializer.validated_data.pop("first_name")
            instance.last_name = serializer.validated_data.pop("last_name")
            instance.profile_pic = serializer.validated_data.pop("profile_pic")
        return instance



class UserDetailView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User
    lookup_field='pk'
    permission_classes = [permissions.AllowAny]
    authentication_classes = [
        authentication.SessionAuthentication,
        TokenAuthentication
    ]


class FollowUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        response = request.user.follow_user(pk)
        return response

class UnFollowUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        response = request.user.unfollow_user(pk)
        return response


from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token


from .utils import remove_none_values,Exception

from user.serializers import RegisterSerializer,LoginSerializer
User = get_user_model()

class UserAuthService:
    @staticmethod
    def register_user(username=None,email=None,password=None):
        register_serializer = RegisterSerializer(
            data=remove_none_values({
                "username": username,
                "email": email,
                "password": password,
            })
        )

        if not register_serializer.is_valid():
            raise Exception(register_serializer.errors)
            
        register_serializer.save()
        token = Token.objects.create(user=register_serializer.instance)

        return {
            "message":"Account created successfully",
            **register_serializer.data, "token":str(token)
            }

    @staticmethod
    def login_user(username, password):
        login_serializer = LoginSerializer(
            data={"username": username, "password":password}
        )

        if not login_serializer.is_valid():
            raise Exception(login_serializer.errors)
        
        login_serializer.save()

        token, val = Token.objects.get_or_create(user=login_serializer.instance)
        return {
            "message": "User successfully logged in",
            **login_serializer.data, "token": str(token)}
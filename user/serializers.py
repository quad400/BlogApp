from rest_framework import serializers,status
from rest_framework.validators import ValidationError

from django.contrib.auth import authenticate
from django.utils import timezone

from .models import User
from core.utils import Exception


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(min_length=8, write_only=True, 
                        required=True, style={"input_type": "password"})

    class Meta:
        model = User
        fields = [
                "id",
                "username",
                "email",
                "password",
                "is_staff",
                "last_login",
                "created_at",
                "updated_at"
        ]

        read_only_fields = [
            "id",
            "is_staff",
            "last_login",
            "created_at",
            "updated_at"
        ]

    def validate(self, attrs):
        if User.objects.filter(email=attrs["email"]).exists():

            raise ValidationError("Email has already been used")
        return super().validate(attrs)

    def create(self, validated_data):
        try:

            password = validated_data.pop("password")
            user = User.objects.create(**validated_data)
            user.set_password(password)
            user.save()

                
        except ValidationError:
            return Exception(
                message="Invalid signup details",
                code=status.HTTP_400_BAD_REQUEST
            )
        return user
        

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, 
                        required=True, style={"input_type": "password"})

    def create(self, validated_data):
        user = authenticate(**validated_data)

        if not user:
            raise Exception(
                message="Invalid username or password",
                code = status.HTTP_401_UNAUTHORIZED,
            )
        user.last_login = timezone.now()
        user.save()

        return user

class UserPublicSerializer(serializers.Serializer):
    username = serializers.CharField(read_only=True)
    id = serializers.UUIDField(read_only=True)
    profile_pic = serializers.ImageField(read_only=True)
    url = serializers.HyperlinkedIdentityField(
                        view_name='profile_detail', lookup_field='pk')


class ProfileSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
                        view_name='profile_detail', lookup_field='pk')

    class Meta:
        model=User
        fields = [
            'url',
            'first_name',
            'last_name',
            'username',
            'email',
            "profile_pic"
        ]


        managed = True
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'


class SoloUserSerializer(serializers.Serializer):
    username = serializers.CharField(read_only=True)
from rest_framework import serializers,status
from rest_framework.validators import ValidationError

from django.contrib.auth import authenticate
from django.utils import timezone

from .models import User,UserFollow
from core.utils import Exception


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(min_length=8, write_only=True, 
                        required=True, style={"input_type": "password"})


    class Meta:
        model = User
        fields = [
                "username",
                "email",
                "password",
                "is_staff",
                "last_login",
                "created_at",
                "updated_at"
        ]

        read_only_fields = [
            "is_staff",
            "last_login",
            "created_at",
            "updated_at"
        ]

    # def validate(self, attrs):
    #     if User.objects.filter(email=attrs["email"]).exists():

    #         raise ValidationError("Email has already been used")
    #     return super().validate(attrs)

    def create(self, validated_data):
            password = validated_data.pop("password")

            user = User.objects.create(**validated_data)
            user.set_password(password)
            user.save()
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
    profile_pic = serializers.ImageField(read_only=True)
    url = serializers.HyperlinkedIdentityField(
                        view_name='user_detail', lookup_field='pk')


class FollowersSerializer(serializers.ModelSerializer):

    follow_by = serializers.SlugRelatedField(read_only=True,slug_field='slug')

    class Meta:
        model = UserFollow
        fields = ['follow_by']
        read_only_fields = ('follow_by')


class FollowingSerializer(serializers.ModelSerializer):

    user = serializers.SlugRelatedField(read_only=True,slug_field='slug')

    class Meta:
        model = UserFollow
        fields = ['user']
        read_only_fields = ('user')



class UserSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField(read_only=True)
    email = serializers.SerializerMethodField(read_only=True)
    following_count = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()

    class Meta:
        model=User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'bio',
            "profile_pic",
            "following_count",
            "followers_count",
            "updated_at",
            "created_at"
        ]


        managed = True
        verbose_name = 'User'
        verbose_name_plural = 'Users'


    def get_username(self, obj):
        return obj.username

    def get_email(self, obj):
        return obj.email

    def get_followers_count(self, obj):
        return obj.followers.all().filter(status='following').count()

    def get_following_count(self, obj):
        return obj.following.all().filter(status='following').count()

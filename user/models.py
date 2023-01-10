import enum
import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,AbstractUser
from django.utils.text import slugify
from django.conf import settings
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND,HTTP_200_OK,HTTP_400_BAD_REQUEST

# User = settings.AUTH_USER_MODEL

class BaseUser(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,unique=True)
    class Meta:
        abstract=True


class User(AbstractUser, BaseUser):
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    username = models.CharField(max_length=100, unique=True, blank=False)
    bio = models.TextField(blank=True, null=True)
    email = models.EmailField(max_length=100, unique=True, blank=False)
    slug = models.SlugField()
    profile_pic = models.ImageField(upload_to='profile', null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def save(self, *args, **kwargs):
        # if not self.pk:
        self.slug = slugify(self.username)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username

    def follow_user(self, id):
        try:
            user_to_follow = User.objects.get(id=id)
        except:
            return Response('User not Found', status=HTTP_404_NOT_FOUND)
        
        if user_to_follow != self:
            try: 
                follow_log = UserFollow.objects.get(
                    user=user_to_follow,follow_by=self
                )
                follow_log.set_followed()
                return Response('Successfully refollowed user', status=HTTP_200_OK)
            except:
                follow_log = UserFollow.objects.create(
                    user=user_to_follow,follow_by=self,
                    status=FollowStatus.following.value
                )
                return Response('Successfully follow user', status=HTTP_200_OK)

        else:
            return Response('You cannot follow yourself', status=HTTP_400_BAD_REQUEST)

    def unfollow_user(self, id):
        try:
            user_to_unfollow = User.objects.get(id=id)
        
        except:
            return Response('User not Found', status=HTTP_404_NOT_FOUND)
        
        if user_to_unfollow != self:
            try:
                unfollow_log = UserFollow.objects.get(
                    user=user_to_unfollow,follow_by=self
                )
                unfollow_log.set_unfollowed()
                return Response('Successfully unfollow user', status=HTTP_200_OK)
            
            except Exception as e:
                return Response('You are not following this user before', status=HTTP_400_BAD_REQUEST)

        else:
            return Response('You cannot unfollow yourself', status=HTTP_400_BAD_REQUEST)


class FollowStatus(enum.Enum):
    following = 'following'
    unfollowed = 'unfollowed'


FOLLOW_STATUS = (
    ('following', 'following'),
    ('unfollowed', 'unfollowed'),
)


class UserFollow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    follow_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers',null=True)
    status = models.CharField(max_length=20,choices=FOLLOW_STATUS, default=FollowStatus.following.value)
    updated_at = models.DateTimeField(auto_now=True)
    followed_at = models.DateTimeField(null=True)
    unfollowed_at = models.DateTimeField(null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user','follow_by'], name='unique_followers')
        ]
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.user} is followed by {self.follow_by}"

    def set_followed(self):
        self.status = FollowStatus.following.value
        self.followed_at = timezone.now()
        self.save()

    def set_unfollowed(self):
        self.status = FollowStatus.unfollowed.value
        self.unfollowed_at = timezone.now()
        self.save()
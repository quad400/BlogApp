from rest_framework import serializers,status
from django.conf import settings

from user.serializers import UserPublicSerializer
from .models import Blog,BlogComment

CATEGORY_TYPE = settings.CATEGORY_TYPE


class BlogCommentSerializer(serializers.Serializer):
    user = serializers.SerializerMethodField(read_only=True)
    created_at = serializers.SerializerMethodField(read_only=True)
    comment = serializers.CharField()

    class Meta:
        model = BlogComment
        fields = [
            'user',
            'comment',
            'created_at',
        ]

    def get_user(self, obj):
        return obj.user.username

    def get_created_at(self, obj):
        return obj.created_at


class BlogSerializer(serializers.ModelSerializer):
    post_user = UserPublicSerializer(read_only=True)
    url = serializers.HyperlinkedIdentityField(view_name='blog_detail', lookup_field='slug')
    is_like = serializers.SerializerMethodField(read_only=True)
    likes_count = serializers.SerializerMethodField(read_only=True)
    comments = BlogCommentSerializer(read_only=True, many=True)

    class Meta:
        model = Blog
        fields = [
            'post_user',
            'url',
            'title',
            'desc',
            'content',
            'category',
            'is_like',
            'likes_count',
            'created_at',
            'updated_at',
            'comments'
        ]

    def validate_category(self, value):
        value = ''.join(value.lower().split())
        
        if value not in CATEGORY_TYPE:
            raise serializers.ValidationError(f"{value} is not a valid category",
                                    code=status.HTTP_400_BAD_REQUEST)

        else:
            return value

    def get_is_like(self, obj):

        is_like = False
        request = self.context.get("request")
        if request:
            user = request.user

            is_like = user in obj.likes.all()
        return is_like

    def get_likes_count(self, obj):
        return obj.likes.count()


class BlogLikeSerializer(serializers.Serializer):
    action = serializers.CharField()
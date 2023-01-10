import enum
from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.status import (
                HTTP_404_NOT_FOUND,
                HTTP_200_OK,
                HTTP_400_BAD_REQUEST,
                HTTP_401_UNAUTHORIZED,    
            )

User = settings.AUTH_USER_MODEL


class BlogQuerySet(models.QuerySet):
    def by_category(self,query):
        qs = self.filter(category__iexact=query)
        return qs

class BlogManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return BlogQuerySet(self.model, using=self._db)


class BlogLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey('Blog', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class BlogComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    blog = models.ForeignKey('Blog', on_delete=models.CASCADE)
    comment = models.CharField(max_length=400)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Blog(models.Model):
    post_user = models.ForeignKey(User,default=1, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100, unique=True)
    desc = models.CharField(max_length=150, blank=True)
    slug = models.SlugField(primary_key=True)
    content = models.TextField()
    category = models.CharField(max_length=25)
    likes = models.ManyToManyField(User, through=BlogLike, related_name='blog_likes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = BlogManager()

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Blog'
        verbose_name_plural = 'Blogs'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)



from django.urls import path

from .views import (BlogListAPI, BlogCreateAPI, 
                    BlogDetailAPI, BlogUpdateAPI,
                    BlogDeleteAPI, BlogLikesAPI,
                    BlogCommentCreateListAPI,
                )

urlpatterns =[
    path('', BlogListAPI.as_view(), name='blog_list'),
    path('create/', BlogCreateAPI.as_view(), name='blog_create'),
    path('<slug:slug>/', BlogDetailAPI.as_view(), name='blog_detail'),
    path('<slug:slug>/update/', BlogUpdateAPI.as_view(), name='blog_update'),
    path('<slug:slug>/delete/', BlogDeleteAPI.as_view(), name='blog_delete'),

    path('<slug:slug>/like/', BlogLikesAPI.as_view()),
    path('<slug:slug>/comment/',BlogCommentCreateListAPI.as_view())
]
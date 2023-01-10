from django.urls import path
from .views import (LoginView, SignUpView,
                    UserUpdateView,UserDetailView,
                    FollowUserView,UnFollowUserView,
                    )


urlpatterns = [
    # authentication
    path('signup/', SignUpView.as_view(), name='sigin-up'),
    path('login/', LoginView.as_view(), name='login'),

    # profile information
    path('user/<slug:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('user/update/<slug:slug>/', UserUpdateView.as_view(), name='user_update'),
    # path('profile/update/<slug:pk>/', ProfileUpdateView.as_view(), name='profile_update'),

    # follow and unfollow
    path('user/<slug:pk>/follow/', FollowUserView.as_view()),
    path('user/<slug:pk>/unfollow/', UnFollowUserView.as_view()),

]
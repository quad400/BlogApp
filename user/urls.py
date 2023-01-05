from django.urls import path
from .views import (LoginView, SignUpView,
                    ProfileUpdateView,ProfileDetailView,
                    
                    )


urlpatterns = [
    # authentication
    path('signup/', SignUpView.as_view(), name='sigin-up'),
    path('login/', LoginView.as_view(), name='login'),

    # profile information
    path('profile/<slug:pk>/', ProfileDetailView.as_view(), name='profile_detail'),
    path('profile/update/<slug:pk>/', ProfileUpdateView.as_view(), name='profile_update'),
]
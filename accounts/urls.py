from django.urls import path , include 
from .views import *



urlpatterns = [
    path('register/',UserCreation.as_view(),name='register'),
    path('login/',LoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view() ,name="profile")
]

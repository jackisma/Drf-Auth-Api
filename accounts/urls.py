from django.urls import path , include 
from .views import UserCreation



urlpatterns = [
    path('register/',UserCreation.as_view(),name='register'),
]

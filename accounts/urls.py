from django.urls import path , include 
from .views import UserCreation,LoginView



urlpatterns = [
    path('register/',UserCreation.as_view(),name='register'),
    path('login/',LoginView.as_view(), name='login'),
]

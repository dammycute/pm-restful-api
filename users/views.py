from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from django.core.mail import send_mail
from .serializers  import *
from .models import CustomUser

# Create your views here.

class UserRegistrationView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    
    def perform_create(self, serializer):
        user =  serializer.save()
        
        send_mail(
            'Your Activation PIN',
            f'Your Activation PIN is {user.activation_pin}',
            'damilolaolawoore03@gmail.com',
            [user.email],
            fail_silently=False,
        )
        

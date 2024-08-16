from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from django.core.mail import send_mail
from rest_framework.permissions import IsAuthenticated
from .serializers  import *
from .models import CustomUser

# Create your views here.

class UserRegistrationView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    
    def create( self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email=serializer.validated_data['email']
        
        try:
            user = CustomUser.objects.get(email=email)
            user.generate_otp()
            send_mail(
                'OTP Verification',
                f'Your Activation PIN is {user.activation_pin}',
                'damilolaolawoore03@gmail.com',
                [user.email],
                fail_silently=False,
            )
            return Response({"message": "OTP sent to your email"}, status=status.HTTP_200_OK)
        
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status = status.HTTP_404_NOT_FOUND)
    


    
        
class ActivationView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = ActivationSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        #Extract email and pin from the validated data
        email = serializer.validated_data['email']
        pin = serializer.validated_data['pin']
        
        try:
            #Retrieve the user email
            user = CustomUser.objects.get(email=email)
            
            #Check if the user's activation pin matches the provided pin
            if user.activation_pin == pin:
                user.is_active = True
                user.activation_pin = None
                user.save()
                
                return Response({'status':'success','detail': 'Account successfully activated'}, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'Invalid activation pin'}, status=status.HTTP_400_BAD_REQUEST)
                
        except CustomUser.DoesNotExist:
            return Response({
                'detail': 'User not found'
            }, status=status.HTTP_404_NOT_FOUND)
            
        except Exception as e:
            return Response({ 'detail': f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    
        

class PasswordResetRequestView(generics.CreateAPIView):
    serializer_class = PasswordResetRequestSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        try:
            user = CustomUser.objects.get(email=email)
            user.generate_otp()
            send_mail(
                'Password Reset OTP',
                f'Your OTP is {user.otp}',
                'noreply@yourdomain.com',
                [user.email],
                fail_silently=False,
            )
            return Response({'message': 'OTP sent to your email'}, status=200)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)
        except Exception as e:
            return Response({'detail': f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class PasswordResetView(generics.CreateAPIView):
    serializer_class = PasswordResetSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        otp = serializer.validated_data['otp']
        new_password = serializer.validated_data['new_password']
        
        try:
            user = CustomUser.objects.get(email=email, otp=otp)
            user.set_password(new_password)
            user.otp = None
            user.save()
            
            return Response({'detail': 'Password has been reset successfully'}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({'error': 'Invalid OTP or email'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'detail': f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        

class ProfileUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user.profile



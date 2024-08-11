from rest_framework import serializers
from .models import CustomUser



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields  = ['email', 'password',]
        
    
    def create(self, vallidated_data):
        user = CustomUser(
            email = vallidated_data['email'],
        )
        user.set_password(vallidated_data['password'])
        user.is_active = False
        user.save()
        user.generate_activation_pin()
        return user
    

class ActivationSerializer(serializers,Serializer):
    email = serializers.EmailField()
    pin = serializers.CharField(max_length=6)
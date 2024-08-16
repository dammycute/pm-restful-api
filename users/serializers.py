from rest_framework import serializers
from .models import * 

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True)
    class Meta:
        model = CustomUser
        fields  = ['id', 'email', 'password',]
        
        
    
    def create(self, vallidated_data):
        user = CustomUser(
            email = vallidated_data['email'],
        )
        user.set_password(vallidated_data['password'])
        user.is_active = False
        user.save()
        user.generate_activation_pin()
        return user
    

class ActivationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    pin = serializers.CharField(max_length=6)
    

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.CharField()
    otp = serializers.CharField(max_length=6)
    new_password = serializers.CharField(write_only=True)
    

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        models = Role
        fields = ['id','name']
        
    
class ProfileSerializer(serializers.ModelSerializer):
    user_role = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Role.objects.all()
    )
    class Meta:
        models = Profile
        fields  = ['first_name', 'last_name', 'user_role', 'profile_pic', 'nationality', ]
        
    def update(self, instance, vallidated_data):
        roles = vallidated_data.pop('user_role', None)
        instance = super().update(instance, vallidated_data)
        if roles is not None:
            instance.user_role.set(roles)
        return instance
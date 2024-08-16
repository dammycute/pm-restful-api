from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
import uuid

# Create your models here.

class CustomUserManager( BaseUserManager):
    def create_user( self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email( email)
        user = self.model( email = email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser( self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_sueruser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Supeuser must have is_staff=True')
        if extra_fields.get( 'is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')
        
        return self.create_user(email, password, **extra_fields)
    

class Role(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=30, blank=True, null=True)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email= models.EmailField(unique=True)
    is_active = models.BooleanField(default = False)
    is_staff = models.BooleanField(default=False)
    activation_pin = models.CharField(max_length = 6, blank=True, null=True)
    date_joined = models.DateTimeField(default=timezone.now)
    otp = models.CharField(max_length=6, blank=True, null=True)
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS  = []
    
    def __str__(self):
        return self.email
    
    def generate_activation_pin(self):
        import random
        pin = ''.join([str(random.randint(0,9)) for _ in range(6)])
        self.activation_pin = pin
        self.save()
        
    def generate_otp(self):
        import random
        pin = ''.join([str(random.randint(0,9)) for _ in range(6)])
        self.otp = pin
        self.save()
        
        
class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=255, blank=True, null=True)
    lastname = models.CharField(max_length = 255, blank=True, null=True)
    profile_pics = models.ImageField(upload_to='profile_pics', blank=True)
    nationality = models.CharField(max_length=50, blank=True, null=True)
    user_role = models.ManyToManyField('Role', blank=True)
    
    
    def __str__(self):
        return self.user.firstname


    

    
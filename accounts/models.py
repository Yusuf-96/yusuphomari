from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

# Create your models here.

Roles = (('admin', 'admin'), ('patients', 'patients'), ('doctors', 'doctors'))
GENDER =[
    ("Male", "Male"),
    ("Female", "Female"),
    ("Other", "Other"),
]

class CustomAccountManager(BaseUserManager):
    def create_superuser(self, email, user_name, first_name,  password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        
        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned to is_superuser=True.')
        
        return self.create_user(email, user_name, first_name, password,  **other_fields)
    
    def create_user(self, email, first_name, user_name,  password, **other_fields):
        if not email:
            raise ValueError(_('You must Provide an email address'))
        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name, first_name = first_name, **other_fields)
        user.set_password(password)
        user.save()
        return user
    
class CustomUser(AbstractBaseUser, PermissionsMixin):
    user_name = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    address = models.CharField(max_length=150)
    email = models.EmailField(max_length=150)
    role = models.CharField(max_length=25, choices=Roles, null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER)
    start_date = models.DateTimeField(default= timezone.now)
    phone = models.CharField(max_length=10, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    
    objects = CustomAccountManager()
    
    USERNAME_FIELD = 'user_name'
    REQUIRED_FIELDS = ['first_name', 'email']
    
    def __str__(self):
        return f'{self.user_name}'
        
        


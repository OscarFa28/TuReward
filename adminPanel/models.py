from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

# Create your models here.
class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    birthday = models.DateField(null=True)
    
    
    NORMAL_USER = 'normal_user'
    ADMINISTRATOR = 'administrator'
    ACCOUNT_TYPE_CHOICES = [
        (NORMAL_USER, 'Normal_user'),
        (ADMINISTRATOR, 'Administrator'),
    ]
    account_type = models.CharField(max_length=50, choices=ACCOUNT_TYPE_CHOICES,  db_index=True)
    
    
    def __str__(self):
        return self.username
    groups = models.ManyToManyField(
        Group,
        related_name='user_group',  
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='user_permissions', 
        blank=True,
    )

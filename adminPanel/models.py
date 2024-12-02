from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
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
    def save(self, *args, **kwargs):
        if self.password:
            self.set_password(self.password)  
        super().save(*args, **kwargs)

class Business(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=15, unique=True)
   
class UserBusinessRelation(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='business_relations')
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='user_relations')
     
class Reward(models.Model):
    title = models.CharField(max_length=25)
    code = models.CharField(max_length=15, unique=True)
    points_requiered = models.PositiveIntegerField()
    description = models.TextField(max_length=250)
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='rewards',)
    
class Transaction(models.Model):
    title = models.CharField(max_length=20)
    amount = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True) 
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='transactions')
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='transactions',)
    
class UserBusinessPoints(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='business_points')
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='user_points')
    points = models.IntegerField(default=0)  

    class Meta:
        unique_together = ['user', 'business'] 
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['business']),
        ]

class UserBusinessRelation(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='business_relations')
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='user_relations')
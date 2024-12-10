from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.auth.hashers import make_password, is_password_usable, check_password
from .utils import generate_qr

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    NORMAL_USER = 'normal_user'
    ADMINISTRATOR = 'administrator'
    ACCOUNT_TYPE_CHOICES = [
        (NORMAL_USER, 'Normal_user'),
        (ADMINISTRATOR, 'Administrator'),
    ]
    code = models.CharField(max_length=15, unique=True, null=True)
    account_type = models.CharField(max_length=50, choices=ACCOUNT_TYPE_CHOICES,  db_index=True)
    qrCode = models.ImageField(upload_to='images/users/qr_codes', blank=True, null=True)
    
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

        if self.pk:  
            current_password = CustomUser.objects.get(pk=self.pk).password
            if self.password != current_password and (not is_password_usable(self.password) or not check_password(self.password, self.password)):
                self.password = make_password(self.password)
                
        else:
            if self.password and not is_password_usable(self.password):
                self.password = make_password(self.password)

        if not self.qrCode:
                    qr_image = generate_qr(self.code)
                    self.qrCode.save(f'QR_code_{self.code}.png', qr_image, save=False)
                    
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username

class Business(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=15, unique=True)
    qrCode = models.ImageField(upload_to='images/business/qr_codes', blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if not self.qrCode:
            qr_image = generate_qr(self.code)
            self.qrCode.save(f'QR_code_{self.code}.png', qr_image, save=False)
        super().save(*args, **kwargs)
        
class UserBusinessRelation(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='business_relations')
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='user_relations')
    points = models.IntegerField(default=0)
    
    class Meta:
        unique_together = ['user', 'business'] 
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['business']),
        ]
        
class Reward(models.Model):
    title = models.CharField(max_length=25)
    code = models.CharField(max_length=15, unique=True)
    points_requiered = models.PositiveIntegerField()
    description = models.TextField(max_length=250)
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='rewards',)
    qrCode = models.ImageField(upload_to='images/rewards/qr_codes', blank=True, null=True)
    
class Transaction(models.Model):
    title = models.CharField(max_length=20)
    amount = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True) 
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='transactions')
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='transactions',)

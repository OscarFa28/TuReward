from django.contrib import admin
from .models import CustomUser, Business, UserBusinessRelation, Reward, Transaction, UserBusinessPoints



@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone_number', 'account_type')
    search_fields = ('username', 'email')
    list_filter = ('account_type',)

@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name',)

@admin.register(UserBusinessRelation)
class UserBusinessRelationAdmin(admin.ModelAdmin):
    list_display = ('user', 'business')
    search_fields = ('user__username', 'business__name')

@admin.register(Reward)
class RewardAdmin(admin.ModelAdmin):
    list_display = ('title', 'code', 'points_requiered', 'business')
    list_filter = ('business',)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('title', 'amount', 'date', 'user', 'business')
    list_filter = ('business', 'date')
    search_fields = ('title',)

@admin.register(UserBusinessPoints)
class UserBusinessPointsAdmin(admin.ModelAdmin):
    list_display = ('user', 'business', 'points')
    list_filter = ('business',)

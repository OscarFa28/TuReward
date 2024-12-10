from rest_framework import serializers
from .models import CustomUser, Reward

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

    def create(self, validated_data):
        
        password = validated_data.pop('password', None)
        user = CustomUser(**validated_data) 
        if password:
            user.set_password(password)  
        user.save()  
        return user

class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, required=True)
    
class RewardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reward
        fields = '__all__'

  
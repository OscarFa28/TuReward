from rest_framework import serializers
from .models import CustomUser, Reward

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = CustomUser.objects.create(**validated_data)
        password = validated_data.pop('password')
        user.set_password(password)
        user.save() 
        return user
    
class RewardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reward
        fields = '__all__'

  
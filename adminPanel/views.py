from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CustomUserSerializer, RewardSerializer
from .models import CustomUser, Business, Reward, UserBusinessPoints, Transaction, UserBusinessRelation
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
import random
import string
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.utils import timezone
from datetime import datetime, timedelta
from django.db import transaction

def is_admin(user):
    return user.is_authenticated and user.account_type == 'administrator'

def is_normal(user):
    return user.is_authenticated and user.account_type == 'normal_user'

@user_passes_test(is_admin)
def index(request):
    user = request.user
    related_businesses = Business.objects.filter(user_relations__user=user)

    businesses_with_rewards = {
        business: Reward.objects.filter(business=business).order_by('points_requiered')
        for business in related_businesses
    }

    context = {
        'user': user,
        'businesses_with_rewards': businesses_with_rewards
    }
    return render(request, "adminIndex.html", context)

@user_passes_test(is_admin)
def scan(request):
    user = request.user

    related_business_relations = UserBusinessRelation.objects.filter(user=user).select_related('business')

    business_transactions = {}
    for relation in related_business_relations:
        business = relation.business
        transactions = Transaction.objects.filter(business=business).select_related('user')
        business_transactions[business] = transactions

    context = {
        'business_transactions': business_transactions,
    }

    return render(request, "adminScan.html", context)


#APIs
class CreateNormalUserAPIView(APIView):
    """
    API to create 'normal_user' account.
    if it do not recieve an account type, it will set normal_user as a account_type
    """
    parser_classes = [FormParser, MultiPartParser, JSONParser]
    def post(self, request, *args, **kwargs):
        user_data = request.data.dict()
        
        if user_data.get('password') != user_data.get('passwordConfirm'):
            return Response(
                {'error': 'Not same passwords'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        account_type = user_data.get('account_type', CustomUser.NORMAL_USER)
        if account_type not in [CustomUser.NORMAL_USER, CustomUser.ADMINISTRATOR]:
            return Response(
                {'error': 'Invalid type of account'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user_data['account_type'] = account_type
        serializer = CustomUserSerializer(data=user_data)
        if serializer.is_valid():
            user = serializer.save()
            code = user_data.get('code', '').strip() 
            if code: 
                try:
                    business = Business.objects.get(code=code)  
                    UserBusinessRelation.objects.create(user=user, business=business) 
                except Business.DoesNotExist:
                    pass
                except Exception as e:
                    pass

            return Response({'message': 'User successfully created.'}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class RewardsAPIView(APIView):
    """
    API to create and delete a new reward for a business.
    only admins of a business can create or delete a new reward
    """
    parser_classes = [FormParser, MultiPartParser, JSONParser]
    
    @method_decorator(user_passes_test(is_admin))  
    def post(self, request, *args, **kwargs):
        user_data = request.data.dict()
        business_id = user_data.get('business')
        title = user_data.get('title', '')
        
        def generate_code(business_name, title, business_code):
            business_code_start = business_name[:3].upper()
            random_numbers_1 = ''.join(random.choices(string.digits, k=3))
            title_code = title[:3].upper()
            random_numbers_2 = ''.join(random.choices(string.digits, k=2))
            business_tail = business_code[-3:].upper()

            return f"{business_code_start}{random_numbers_1}{title_code}{random_numbers_2}{business_tail}"
        
        try:
            business = Business.objects.get(id=business_id)
            business_name = business.name
            business_code = business.code
            
            user_data['code'] = generate_code(business_name, title, business_code)
            user_data['business'] = business.id
        except Business.DoesNotExist:
            return Response({'error': 'Business not found.'}, status=status.HTTP_404_NOT_FOUND)

        print(user_data)
        serializer = RewardSerializer(data=user_data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'New reward created.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @method_decorator(user_passes_test(is_admin))
    def delete(self, request, *args, **kwargs):
        
        if request.content_type == 'application/json':
            data = JSONParser().parse(request)
        else:
            return Response({'error': 'Unsupported media type'}, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
        
        reward_id = data.get('reward_id')
        
        try:
            reward = Reward.objects.get(id=reward_id)
            reward.delete() 
            return Response({'message': 'Reward deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
        except Reward.DoesNotExist:
            return Response({'error': 'Reward not found.'}, status=status.HTTP_404_NOT_FOUND)
        
class CheckCodeApiView(APIView):
    permission_classes = [is_admin]

    def get(self, request, *args, **kwargs):
        code = request.GET.get('code')
        
        if not code or "#" not in code:
            return Response({'error': 'Invalid or missing code.'}, status=status.HTTP_400_BAD_REQUEST)

        parts = code.split("#")
        if len(parts) != 2:
            return Response({'error': 'Invalid code format.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            reward = Reward.objects.get(code=parts[0])
            customer = CustomUser.objects.get(id=parts[1])
            customer_points = UserBusinessPoints.objects.get(user=customer, business=reward.business)
        except Reward.DoesNotExist:
            return Response({'error': 'Reward not found.'}, status=status.HTTP_404_NOT_FOUND)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        except UserBusinessPoints.DoesNotExist:
            return Response({'error': 'User does not have points with this business.'}, status=status.HTTP_404_NOT_FOUND)

        
        if not UserBusinessRelation.objects.filter(user=request.user, business=reward.business).exists():
            return Response({'error': 'You are not authorized to redeem rewards for this business.'}, status=status.HTTP_403_FORBIDDEN)

        if reward.points_requiered > customer_points.points:
            return Response({'error': 'The user does not have enough points.'}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            customer_points.points -= reward.points_requiered
            customer_points.save()
            Transaction.objects.create(
                title='Points spent',
                amount=reward.points_requiered,
                user=customer,
                business=reward.business
            )

        return Response(status=status.HTTP_200_OK)

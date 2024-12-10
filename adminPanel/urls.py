from django.urls import path

from adminPanel import views
from .views import CreateNormalUserAPIView, RewardsAPIView, CheckCodeApiView, AddBusinessApiView, UpdatePersonalInfoApiView

app_name = 'adminPanel'

urlpatterns = [
    path('',views.index, name="home"),
    path('scan/',views.scan, name="scan"),
    #APIs
    path('create-normal-user/', CreateNormalUserAPIView.as_view(), name='create-normal-user'),
    path('rewards-api/', RewardsAPIView.as_view(), name='rewards-api'),
    path('check-code-api/', CheckCodeApiView.as_view(), name='check-code-api'),
    path('add-business-api/', AddBusinessApiView.as_view(), name='add-business-api'),
    path('update-personal-info-api/', UpdatePersonalInfoApiView.as_view(), name='update-personal-info-api'),
]
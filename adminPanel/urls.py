from django.urls import path

from adminPanel import views
from .views import CreateNormalUserAPIView, RewardsAPIView, CheckCodeApiView

app_name = 'adminPanel'

urlpatterns = [
    path('',views.index, name="home"),
    path('scan/',views.scan, name="scan"),
    #APIs
    path('create-normal-user/', CreateNormalUserAPIView.as_view(), name='create-normal-user'),
    path('rewards-api/', RewardsAPIView.as_view(), name='rewards-api'),
    path('check-code-api/', CheckCodeApiView.as_view(), name='check-code-api'),
]
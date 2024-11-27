from django.urls import path

from userPanel import views


app_name = 'userPanel'

urlpatterns = [
    path('',views.userIndex, name="home"),
    
    
]
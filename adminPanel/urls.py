from django.urls import path

from adminPanel import views


app_name = 'adminPanel'

urlpatterns = [
    path('',views.index, name="home"),
    path('usersModifyApi',views.usersModifyApi, name="usersModifyApi"),
    
    
]
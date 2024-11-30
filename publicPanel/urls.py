from django.urls import path

from publicPanel import views


app_name = 'publicPanel'

urlpatterns = [
    path('',views.index, name="home"),
    path('signUp/',views.signUp, name="signUp"),
    
    #APIs
    path('usersApi/',views.usersApi, name="users-api"),
    
]
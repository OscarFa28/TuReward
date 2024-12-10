from django.shortcuts import render
from rest_framework import serializers
from django.shortcuts import redirect

def index(request):
    
    return render(request, "index.html")

def signUp(request):
    
    return render(request, "create_account.html")

def redirect_panel(request):
    user = request.user
    if user.account_type == 'administrator':
        return redirect('adminPanel:home')
    if user.account_type == 'normal_user':
        return redirect('userPanel:home')

    
    

#APIs
def usersApi(request):
    
    return render(request, "create_account.html")
from django.shortcuts import render
from rest_framework import serializers

def index(request):
    
    return render(request, "index.html")

def signUp(request):
    
    return render(request, "create_account.html")



#APIs
def usersApi(request):
    
    return render(request, "create_account.html")
from django.shortcuts import render


def userIndex(request):
    
    return render(request, "userIndex.html")
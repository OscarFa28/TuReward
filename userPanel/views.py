from django.shortcuts import render


def userIndex(request):
    
    return render(request, "userIndex.html")

def userOptions(request):
    
    return render(request, "userOptions.html")
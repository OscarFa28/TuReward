from django.shortcuts import render

def index(request):
    
    return render(request, "adminIndex.html")


#APIs
def usersModifyApi(request):
    
    return render(request, "create_account.html")
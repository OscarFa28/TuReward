from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from adminPanel.models import CustomUser, UserBusinessRelation, Reward, Transaction

def is_admin(user):
    return user.is_authenticated and user.account_type == 'administrator'

def is_normal(user):
    return user.is_authenticated and user.account_type == 'normal_user'

@user_passes_test(is_normal)
def userIndex(request):
    user = request.user
    
    # Obtén las relaciones de negocios del usuario
    user_business_relations = UserBusinessRelation.objects.filter(user=user)
    
    # Crea un diccionario para almacenar los negocios, recompensas y puntos
    businesses_data = []
    
    for relation in user_business_relations:
        business = relation.business
        rewards = business.rewards.all()
        transactions = Transaction.objects.filter(user=user, business=business)
        
        # Obtén los puntos del usuario para este negocio
        points = relation.points
        
        # Agregar los datos al diccionario
        businesses_data.append({
            "business": business,
            "rewards": rewards,
            "transactions": transactions,
            "points": points,
        })
    
    # Pasar los datos al contexto
    context = {
        "user": user,
        "businesses_data": businesses_data,
    }

    return render(request, "userIndex.html", context)

@user_passes_test(is_normal)
def userOptions(request):
    context = {
        'user': request.user,
    }
    return render(request, "userOptions.html", context)
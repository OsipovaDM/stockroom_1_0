# decorators.py
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect
from .models import UserProfile

def role_required(allowed_roles):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            
            try:
                profile = request.user.userprofile
                if profile.role not in allowed_roles:
                    return redirect('home')
            except UserProfile.DoesNotExist:
                return redirect('home')
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

# Декораторы для конкретных ролей
client_required = role_required(['client', 'worker', 'admin'])
worker_required = role_required(['worker', 'admin'])
admin_required = role_required(['admin'])
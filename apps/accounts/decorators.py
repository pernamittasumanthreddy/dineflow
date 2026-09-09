"""Granular Role & Module Permission Decorators."""
from functools import wraps
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.contrib import messages

def role_required(*allowed_roles):
    """
    Decorator for views that checks whether the user has at least one of the required roles.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('accounts:login')
            if request.user.is_superuser or request.user.role in allowed_roles:
                return view_func(request, *args, **kwargs)
            messages.error(request, "You do not have permission to access this resource.")
            raise PermissionDenied("Access Denied: Insufficient Role Privileges")
        return _wrapped_view
    return decorator

def module_permission_required(module_name):
    """
    Decorator verifying whether user's role has permission to the designated module.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('accounts:login')
            if request.user.has_module_permission(module_name):
                return view_func(request, *args, **kwargs)
            messages.error(request, f"Access to '{module_name.title()}' module is restricted for your role.")
            raise PermissionDenied(f"Access Denied for module '{module_name}'")
        return _wrapped_view
    return decorator

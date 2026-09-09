from functools import wraps
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

def get_user_role_code(user):
    """
    Safely retrieves the role code for an authenticated user.
    """
    if not user or not user.is_authenticated:
        return None
    try:
        return user.userprofile.role.code
    except Exception:
        if user.is_superuser:
            return 'super_admin'
        return None

def role_required(allowed_roles):
    """
    Enforces that the authenticated user belongs to one of the permitted roles.
    If unauthenticated, redirects to Role Selection / Login with ?next=...
    If unauthorized, returns HTTP 403 Forbidden with custom Access Denied page.
    """
    if isinstance(allowed_roles, str):
        allowed_roles = [allowed_roles]

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect(f'/accounts/role-select/?next={request.path}')
            
            user_role = get_user_role_code(request.user)
            
            if user_role in allowed_roles or (request.user.is_superuser and 'super_admin' in allowed_roles):
                return view_func(request, *args, **kwargs)
            
            # Access Denied for unauthorized role
            context = {
                'page_title': '403 Access Denied — Insufficient Permissions',
                'user_role': user_role,
                'allowed_roles': allowed_roles,
                'attempted_path': request.path,
            }
            return render(request, 'errors/403.html', context, status=403)
        return _wrapped_view
    return decorator

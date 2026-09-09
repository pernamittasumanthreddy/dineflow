from django.shortcuts import redirect
from django.urls import reverse

class RBACAuthMiddleware:
    """
    Enterprise RBAC Middleware for DineFlow:
    Ensures that unauthenticated requests to protected dashboards and operational
    modules are immediately redirected to the Role Selection / Login portal.
    """
    def __init__(self, get_response):
        self.get_response = get_response

        self.public_path_prefixes = [
            '/accounts/role-select',
            '/accounts/login',
            '/accounts/logout',
            '/accounts/register',
            '/accounts/forgot-password',
            '/accounts/otp-verify',
            '/landing/',
            '/static/',
            '/admin/',
        ]

    def __call__(self, request):
        path = request.path

        # Root route handling
        if path == '/':
            if request.user.is_authenticated:
                try:
                    dashboard_url = request.user.userprofile.role.dashboard_url
                    return redirect(dashboard_url)
                except Exception:
                    return redirect('/dashboard/owner/')
            else:
                return redirect('/accounts/role-select/')

        # Check if path is public
        is_public = any(path.startswith(prefix) for prefix in self.public_path_prefixes)

        # If not authenticated and trying to access protected paths
        if not is_public and not request.user.is_authenticated:
            return redirect(f'/accounts/role-select/?next={path}')

        response = self.get_response(request)
        return response

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
from apps.accounts.models import Role, UserProfile, LoginHistory, AuditLog
from apps.accounts.seeder import seed_roles_and_users

def ensure_roles_seeded():
    """Helper to verify roles and default users are populated."""
    if Role.objects.count() < 10:
        seed_roles_and_users()

def role_select_view(request):
    """
    Step 1 of Authentication: Pre-Login Role Selection Portal.
    If already authenticated, redirects directly to user's assigned dashboard.
    """
    if request.user.is_authenticated:
        try:
            return redirect(request.user.userprofile.role.dashboard_url)
        except Exception:
            return redirect('/dashboard/owner/')

    ensure_roles_seeded()
    roles = Role.objects.filter(is_active=True).order_by('id')
    signed_out = request.GET.get('signed_out', False)
    next_url = request.GET.get('next', '')

    context = {
        'roles': roles,
        'signed_out': signed_out,
        'next_url': next_url,
        'page_title': 'Select Role — DineFlow ERP',
    }
    return render(request, 'accounts/role_select.html', context)

@csrf_protect
def login_view(request, role_code=None):
    """
    Step 2 of Authentication: Role-Specific Login.
    Enforces real Django authentication and verifies that credentials belong to selected role.
    """
    if request.user.is_authenticated:
        try:
            return redirect(request.user.userprofile.role.dashboard_url)
        except Exception:
            return redirect('/dashboard/owner/')

    ensure_roles_seeded()
    
    # Extract role from URL or query param or form
    target_role_code = role_code or request.GET.get('role') or request.POST.get('role', 'owner')
    selected_role = Role.objects.filter(code=target_role_code, is_active=True).first()
    
    if not selected_role:
        return redirect('/accounts/role-select/')

    error_message = None
    next_url = request.GET.get('next') or request.POST.get('next', '')

    if request.method == 'POST':
        username_or_email = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        client_ip = request.META.get('REMOTE_ADDR')
        user_agent = request.META.get('HTTP_USER_AGENT', '')

        # 1. Attempt standard authentication
        user = authenticate(request, username=username_or_email, password=password)

        # 2. Fallback check if user entered email instead of username
        if user is None and '@' in username_or_email:
            matched_user = User.objects.filter(email__iexact=username_or_email).first()
            if matched_user:
                user = authenticate(request, username=matched_user.username, password=password)

        # 3. Check credentials validity
        if user is None:
            LoginHistory.objects.create(
                user=None,
                username_attempted=username_or_email,
                role_attempted=selected_role.code,
                ip_address=client_ip,
                user_agent=user_agent,
                status='FAILED_CREDENTIALS'
            )
            error_message = "Invalid username/email or password. Please verify your credentials."
        else:
            # 4. Check role alignment
            user_profile = getattr(user, 'userprofile', None)
            user_role_code = user_profile.role.code if user_profile and user_profile.role else None

            if not user.is_superuser and user_role_code != selected_role.code:
                LoginHistory.objects.create(
                    user=user,
                    username_attempted=username_or_email,
                    role_attempted=selected_role.code,
                    ip_address=client_ip,
                    user_agent=user_agent,
                    status='FAILED_ROLE_MISMATCH'
                )
                actual_role_name = user_profile.role.name if user_profile and user_profile.role else 'Unknown'
                error_message = f"These credentials do not belong to the selected role '{selected_role.name}'. (Assigned Role: {actual_role_name})"
            else:
                # 5. Successful Authentication
                login(request, user)
                LoginHistory.objects.create(
                    user=user,
                    username_attempted=username_or_email,
                    role_attempted=selected_role.code,
                    ip_address=client_ip,
                    user_agent=user_agent,
                    status='SUCCESS'
                )
                AuditLog.objects.create(
                    user=user,
                    action='USER_LOGIN',
                    module='AUTHENTICATION',
                    details=f"User signed in as {selected_role.name} from {client_ip}",
                    ip_address=client_ip
                )

                # Set session branch if available
                if user_profile and user_profile.branch:
                    request.session['dineflow_active_branch'] = user_profile.branch

                # Redirect to destination
                if next_url and next_url.startswith('/'):
                    return redirect(next_url)
                return redirect(selected_role.dashboard_url)

    # Pre-configured default credentials for role
    default_user = User.objects.filter(userprofile__role=selected_role).first()

    context = {
        'selected_role': selected_role,
        'role_code': selected_role.code,
        'error_message': error_message,
        'next_url': next_url,
        'default_username': default_user.username if default_user else '',
        'default_email': default_user.email if default_user else '',
        'page_title': f'{selected_role.name} Sign In — DineFlow',
    }
    return render(request, 'accounts/login.html', context)

def logout_view(request):
    """
    Step 3 of Authentication: Secure Django Logout.
    Destroys authenticated session, clears auth state, and redirects to Role Selection.
    """
    if request.user.is_authenticated:
        AuditLog.objects.create(
            user=request.user,
            action='USER_LOGOUT',
            module='AUTHENTICATION',
            details=f"User logged out successfully.",
            ip_address=request.META.get('REMOTE_ADDR')
        )
    logout(request)
    request.session.flush()
    return redirect('/accounts/role-select/?signed_out=1')

def register_view(request):
    """
    Restaurant Outlet Registration.
    """
    if request.method == 'POST':
        return redirect('/accounts/role-select/')
    return render(request, 'accounts/register.html', {'page_title': 'Register Outlet — DineFlow'})

def forgot_password_view(request):
    """
    Password Reset.
    """
    return render(request, 'accounts/forgot_password.html', {'page_title': 'Reset Password — DineFlow'})

def otp_verify_view(request):
    """
    SMS/WhatsApp OTP Verification.
    """
    return render(request, 'accounts/otp_verify.html', {'page_title': 'OTP Verification — DineFlow'})

def custom_403_view(request, exception=None):
    """
    Custom 403 Forbidden / Access Denied Page.
    """
    return render(request, 'errors/403.html', {'page_title': '403 Access Denied — DineFlow'}, status=403)

def custom_404_view(request, exception=None):
    return render(request, 'errors/404.html', {'page_title': '404 Page Not Found — DineFlow'}, status=404)

def custom_500_view(request):
    return render(request, 'errors/500.html', {'page_title': '500 Server Error — DineFlow'}, status=500)

def session_timeout_view(request):
    return render(request, 'errors/session_timeout.html', {'page_title': 'Session Timed Out — DineFlow'})

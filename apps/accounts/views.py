"""Authentication, Role Governance, and Session Controller Views."""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from apps.accounts.models import User, LoginHistory, RoleChoices
from apps.accounts.forms import UserLoginForm, UserRegistrationForm, UserProfileUpdateForm
from apps.accounts.decorators import role_required, module_permission_required
from apps.audit.middleware import get_client_ip

def login_view(request):
    """
    Secure enterprise login view.
    Includes brute-force lockout, LoginHistory auditing, and role-based redirect.
    """
    if request.user.is_authenticated:
        return redirect('core:dashboard')

    form = UserLoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        identifier = form.cleaned_data['email_or_username']
        password = form.cleaned_data['password']
        ip = get_client_ip(request)
        ua = request.META.get('HTTP_USER_AGENT', '')[:500]

        user = None
        # Support email or username
        try:
            user_obj = User.objects.get(Q(email__iexact=identifier) | Q(username__iexact=identifier))
            if user_obj.is_locked:
                LoginHistory.objects.create(
                    user=user_obj, attempted_email=identifier,
                    ip_address=ip, user_agent=ua, status='LOCKED'
                )
                messages.error(request, "Your account is temporarily locked due to excessive failed attempts. Contact Manager.")
                return render(request, 'accounts/login.html', {'form': form})
            
            user = User.objects.filter(id=user_obj.id).first()
            if not user.check_password(password):
                user.failed_login_attempts += 1
                if user.failed_login_attempts >= 5:
                    user.is_locked = True
                user.save(update_fields=['failed_login_attempts', 'is_locked'])
                LoginHistory.objects.create(
                    user=user, attempted_email=identifier,
                    ip_address=ip, user_agent=ua, status='FAILED'
                )
                messages.error(request, "Invalid credentials. Please try again.")
                return render(request, 'accounts/login.html', {'form': form})
        except User.DoesNotExist:
            LoginHistory.objects.create(
                user=None, attempted_email=identifier,
                ip_address=ip, user_agent=ua, status='FAILED'
            )
            messages.error(request, "Invalid credentials. Please try again.")
            return render(request, 'accounts/login.html', {'form': form})

        if user and user.is_active:
            user.failed_login_attempts = 0
            user.last_login_ip = ip
            user.save(update_fields=['failed_login_attempts', 'last_login_ip'])
            login(request, user)
            LoginHistory.objects.create(
                user=user, attempted_email=identifier,
                ip_address=ip, user_agent=ua, status='SUCCESS'
            )
            messages.success(request, f"Welcome back, {user.display_name}!")
            next_url = request.GET.get('next') or 'core:dashboard'
            return redirect(next_url)
        else:
            messages.error(request, "This account is disabled.")

    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    """Secure logout view terminating the active session."""
    logout(request)
    messages.info(request, "You have been logged out securely.")
    return redirect('accounts:login')

@login_required
def profile_view(request):
    """User profile details and avatar update."""
    user = request.user
    form = UserProfileUpdateForm(request.POST or None, request.FILES or None, instance=user)
    pwd_form = PasswordChangeForm(user, request.POST or None)

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'update_profile' and form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('accounts:profile')
        elif action == 'change_password' and pwd_form.is_valid():
            user = pwd_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Password changed successfully.")
            return redirect('accounts:profile')

    return render(request, 'accounts/profile.html', {
        'form': form,
        'pwd_form': pwd_form,
    })

@login_required
@module_permission_required('settings')
def user_list_view(request):
    """Directory of all users with role and branch filters."""
    users = User.objects.all().select_related('restaurant', 'branch').order_by('-created_at')
    
    role_filter = request.GET.get('role')
    search_query = request.GET.get('q')
    
    if role_filter:
        users = users.filter(role=role_filter)
    if search_query:
        users = users.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(phone_number__icontains=search_query)
        )

    roles = RoleChoices.choices
    return render(request, 'accounts/users_list.html', {
        'users': users,
        'roles': roles,
        'selected_role': role_filter,
        'search_query': search_query,
    })

@login_required
@module_permission_required('settings')
def user_create_view(request):
    """Manager / Admin creation of staff or customer accounts."""
    form = UserRegistrationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        new_user = form.save(commit=False)
        new_user.set_password(form.cleaned_data['password'])
        new_user.save()
        messages.success(request, f"User {new_user.email} created successfully.")
        return redirect('accounts:user_list')
    return render(request, 'accounts/user_form.html', {'form': form, 'title': 'Create New User'})

@login_required
@module_permission_required('settings')
def user_toggle_lock_view(request, user_id):
    """Unlock or lock an account."""
    target_user = get_object_or_404(User, id=user_id)
    target_user.is_locked = not target_user.is_locked
    if not target_user.is_locked:
        target_user.failed_login_attempts = 0
    target_user.save(update_fields=['is_locked', 'failed_login_attempts'])
    messages.success(request, f"Updated lock status for {target_user.display_name}.")
    return redirect('accounts:user_list')

@login_required
@module_permission_required('settings')
def login_history_view(request):
    """Audit log of authentication events."""
    histories = LoginHistory.objects.all().select_related('user').order_by('-timestamp')[:100]
    return render(request, 'accounts/login_history.html', {'histories': histories})

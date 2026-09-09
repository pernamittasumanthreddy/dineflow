from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def login_view(request):
    """
    Role-aware authentication page with quick role access.
    """
    if request.method == 'POST':
        role = request.POST.get('role', 'owner')
        request.session['dineflow_active_role'] = role
        return redirect(f'/dashboard/{role}/')
    signed_out = request.GET.get('signed_out', False)
    return render(request, 'accounts/login.html', {'signed_out': signed_out})

def logout_view(request):
    """
    Sign out user, flush active session, and redirect to login page.
    """
    request.session.flush()
    return redirect('/accounts/login/?signed_out=1')

def register_view(request):
    """
    Restaurant Registration (GSTIN, FSSAI license, Branch details).
    """
    if request.method == 'POST':
        request.session['dineflow_active_role'] = 'owner'
        return redirect('/dashboard/owner/')
    return render(request, 'accounts/register.html')

def forgot_password_view(request):
    """
    Password reset request via Registered Email or Indian Mobile (+91).
    """
    return render(request, 'accounts/forgot_password.html')

def otp_verify_view(request):
    """
    6-Digit SMS / WhatsApp OTP verification screen.
    """
    if request.method == 'POST':
        return redirect('/dashboard/owner/')
    return render(request, 'accounts/otp_verify.html')

def profile_view(request):
    """
    User Profile & Security Settings.
    """
    return render(request, 'accounts/profile.html')

@csrf_exempt
def switch_role_api(request):
    """
    Interactive AJAX role switcher for ERP user roles.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            role = data.get('role', 'owner')
            request.session['dineflow_active_role'] = role
            return JsonResponse({'status': 'ok', 'redirect_url': f'/dashboard/{role}/'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'invalid_method'}, status=405)

@csrf_exempt
def switch_branch_api(request):
    """
    Interactive AJAX branch switcher.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            branch = data.get('branch', 'Indiranagar Main (Bangalore)')
            request.session['dineflow_active_branch'] = branch
            return JsonResponse({'status': 'ok'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'invalid_method'}, status=405)

# Error Page Views
def custom_404_view(request, exception=None):
    return render(request, 'errors/404.html', status=404)

def custom_403_view(request, exception=None):
    return render(request, 'errors/403.html', status=403)

def custom_500_view(request):
    return render(request, 'errors/500.html', status=500)

def session_timeout_view(request):
    return render(request, 'errors/session_timeout.html')

def unauthorized_view(request):
    return render(request, 'errors/403.html')

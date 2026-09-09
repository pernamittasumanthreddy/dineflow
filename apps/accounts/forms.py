"""Authentication and User Management Forms."""
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from apps.accounts.models import User, RoleChoices
from apps.branches.models import Branch

class UserLoginForm(forms.Form):
    """Secure login form supporting email or username."""
    email_or_username = forms.CharField(
        label="Email or Username",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter email or username',
            'autofocus': True,
            'autocomplete': 'username'
        })
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password',
            'autocomplete': 'current-password'
        })
    )

class UserRegistrationForm(forms.ModelForm):
    """Staff and Customer registration form."""
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Strong password'}),
        validators=[validate_password]
    )
    confirm_password = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Repeat password'})
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'role', 'branch']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'name@dineflow.internal'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+91 9876543210'}),
            'role': forms.Select(attrs={'class': 'form-select'}),
            'branch': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        pwd = cleaned_data.get('password')
        confirm_pwd = cleaned_data.get('confirm_password')
        if pwd and confirm_pwd and pwd != confirm_pwd:
            self.add_error('confirm_password', "Passwords do not match.")
        return cleaned_data

class UserProfileUpdateForm(forms.ModelForm):
    """Profile editing form."""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number', 'avatar']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
        }

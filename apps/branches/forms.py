"""Branch Management Forms."""
from django import forms
from apps.branches.models import Branch

class BranchForm(forms.ModelForm):
    class Meta:
        model = Branch
        fields = [
            'name', 'code', 'manager', 'phone', 'email',
            'address', 'city', 'state', 'pincode',
            'opening_time', 'closing_time', 'total_seating_capacity', 'is_active'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Banjara Hills Flagship'}),
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'BH-01'}),
            'manager': forms.Select(attrs={'class': 'form-select'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'pincode': forms.TextInput(attrs={'class': 'form-control'}),
            'opening_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'closing_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'total_seating_capacity': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

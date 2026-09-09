"""Table Booking & Reservation Forms."""
from django import forms
from apps.reservations.models import Reservation, ReservationStatus

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = [
            'guest_name', 'guest_phone', 'guest_email',
            'reservation_date', 'reservation_time', 'guest_count',
            'assigned_table', 'status', 'special_requests'
        ]
        widgets = {
            'guest_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'guest_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+91 9876543210'}),
            'guest_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'guest@example.com'}),
            'reservation_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'reservation_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'guest_count': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'assigned_table': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'special_requests': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'e.g. Birthday anniversary, high chair needed, window seat'}),
        }

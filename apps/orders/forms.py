"""Order Management and POS Forms."""
from django import forms
from apps.orders.models import Order, OrderItem, OrderType, OrderStatus

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['order_type', 'table', 'customer', 'guest_count', 'special_instructions']
        widgets = {
            'order_type': forms.Select(attrs={'class': 'form-select'}),
            'table': forms.Select(attrs={'class': 'form-select'}),
            'customer': forms.Select(attrs={'class': 'form-select'}),
            'guest_count': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'special_instructions': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

class OrderCancelForm(forms.Form):
    reason = forms.CharField(
        label="Reason for Cancellation",
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Provide mandatory explanation for cancellation audit'
        }),
        required=True
    )

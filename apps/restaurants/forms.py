"""Restaurant and Business Profile Forms."""
from django import forms
from apps.restaurants.models import Restaurant, RestaurantSetting

class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = [
            'name', 'legal_entity_name', 'gstin', 'fssai_number',
            'email', 'phone', 'website', 'address_line1', 'address_line2',
            'city', 'state', 'pincode', 'country', 'opening_time', 'closing_time', 'logo'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'legal_entity_name': forms.TextInput(attrs={'class': 'form-control'}),
            'gstin': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 36AAAAA0000A1Z5'}),
            'fssai_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '14-digit FSSAI'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
            'address_line1': forms.TextInput(attrs={'class': 'form-control'}),
            'address_line2': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'pincode': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'opening_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'closing_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'logo': forms.FileInput(attrs={'class': 'form-control'}),
        }

class RestaurantSettingForm(forms.ModelForm):
    class Meta:
        model = RestaurantSetting
        fields = [
            'default_cgst_percent', 'default_sgst_percent', 'default_service_charge_percent',
            'is_tax_inclusive', 'invoice_prefix', 'bill_footer_message',
            'enable_table_reservations', 'enable_kds', 'enable_delivery_dispatch',
            'low_stock_alert_threshold'
        ]
        widgets = {
            'default_cgst_percent': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'default_sgst_percent': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'default_service_charge_percent': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'is_tax_inclusive': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'invoice_prefix': forms.TextInput(attrs={'class': 'form-control'}),
            'bill_footer_message': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'enable_table_reservations': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'enable_kds': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'enable_delivery_dispatch': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'low_stock_alert_threshold': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
        }

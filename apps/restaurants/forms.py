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
            'name': forms.TextInput(attrs={'class': 'df-form-control'}),
            'legal_entity_name': forms.TextInput(attrs={'class': 'df-form-control'}),
            'gstin': forms.TextInput(attrs={'class': 'df-form-control', 'placeholder': 'e.g. 36AAAAA0000A1Z5'}),
            'fssai_number': forms.TextInput(attrs={'class': 'df-form-control', 'placeholder': '14-digit FSSAI'}),
            'email': forms.EmailInput(attrs={'class': 'df-form-control'}),
            'phone': forms.TextInput(attrs={'class': 'df-form-control'}),
            'website': forms.URLInput(attrs={'class': 'df-form-control'}),
            'address_line1': forms.TextInput(attrs={'class': 'df-form-control'}),
            'address_line2': forms.TextInput(attrs={'class': 'df-form-control'}),
            'city': forms.TextInput(attrs={'class': 'df-form-control'}),
            'state': forms.TextInput(attrs={'class': 'df-form-control'}),
            'pincode': forms.TextInput(attrs={'class': 'df-form-control'}),
            'country': forms.TextInput(attrs={'class': 'df-form-control'}),
            'opening_time': forms.TimeInput(attrs={'class': 'df-form-control', 'type': 'time'}),
            'closing_time': forms.TimeInput(attrs={'class': 'df-form-control', 'type': 'time'}),
            'logo': forms.FileInput(attrs={'class': 'df-form-control'}),
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
            'default_cgst_percent': forms.NumberInput(attrs={'class': 'df-form-control', 'step': '0.01'}),
            'default_sgst_percent': forms.NumberInput(attrs={'class': 'df-form-control', 'step': '0.01'}),
            'default_service_charge_percent': forms.NumberInput(attrs={'class': 'df-form-control', 'step': '0.01'}),
            'is_tax_inclusive': forms.CheckboxInput(attrs={'class': 'df-form-check-input'}),
            'invoice_prefix': forms.TextInput(attrs={'class': 'df-form-control'}),
            'bill_footer_message': forms.Textarea(attrs={'class': 'df-form-control', 'rows': 2}),
            'enable_table_reservations': forms.CheckboxInput(attrs={'class': 'df-form-check-input'}),
            'enable_kds': forms.CheckboxInput(attrs={'class': 'df-form-check-input'}),
            'enable_delivery_dispatch': forms.CheckboxInput(attrs={'class': 'df-form-check-input'}),
            'low_stock_alert_threshold': forms.NumberInput(attrs={'class': 'df-form-control', 'step': '0.1'}),
        }

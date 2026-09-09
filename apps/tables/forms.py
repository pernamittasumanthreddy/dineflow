"""Floor Plan and Table Management Forms."""
from django import forms
from apps.tables.models import FloorSection, RestaurantTable, TableStatus

class FloorSectionForm(forms.ModelForm):
    class Meta:
        model = FloorSection
        fields = ['name', 'floor_number', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. AC Family Section'}),
            'floor_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

class RestaurantTableForm(forms.ModelForm):
    class Meta:
        model = RestaurantTable
        fields = ['section', 'table_number', 'seating_capacity', 'status']
        widgets = {
            'section': forms.Select(attrs={'class': 'form-select'}),
            'table_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. T-12'}),
            'seating_capacity': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

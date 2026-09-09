"""Menu and Dish Management Forms."""
from django import forms
from apps.menu.models import Category, MenuItem, MenuItemVariant, MenuItemAddon, RecipeItem

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'slug', 'description', 'display_order', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Biryani, Curries, Dosa'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'biryani'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'display_order': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }

class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = [
            'category', 'name', 'code', 'description', 'food_type', 'spice_level',
            'base_price', 'cost_price', 'tax_rate_percent', 'preparation_time_minutes',
            'is_available', 'is_featured', 'image'
        ]
        widgets = {
            'category': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Hyderabadi Chicken Dum Biryani'}),
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'SKU-BIR-01'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'food_type': forms.Select(attrs={'class': 'form-select'}),
            'spice_level': forms.Select(attrs={'class': 'form-select'}),
            'base_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'cost_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'tax_rate_percent': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'preparation_time_minutes': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }

class MenuItemVariantForm(forms.ModelForm):
    class Meta:
        model = MenuItemVariant
        fields = ['name', 'price', 'is_default']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Single / Full / Family Pack'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'is_default': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class MenuItemAddonForm(forms.ModelForm):
    class Meta:
        model = MenuItemAddon
        fields = ['name', 'price']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Extra Mirchi Ka Salan'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

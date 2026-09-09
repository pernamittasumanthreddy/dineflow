"""Restaurant Profile and Configuration Views."""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.restaurants.models import Restaurant, RestaurantSetting
from apps.restaurants.forms import RestaurantForm, RestaurantSettingForm
from apps.accounts.decorators import role_required, module_permission_required
from apps.accounts.models import RoleChoices

@login_required
@module_permission_required('settings')
def restaurant_profile_view(request):
    """View and update restaurant corporate entity profile."""
    restaurant = Restaurant.objects.first()
    if not restaurant:
        restaurant = Restaurant.objects.create(
            name="The Royal Nizam & Spice Lounge",
            slug="royal-nizam-lounge",
            legal_entity_name="Nizam Hospitality Private Limited",
            gstin="36AAACN1234F1Z9",
            fssai_number="13624014000189",
            email="contact@royalnizam.in",
            phone="+91 40 2334 5678",
            address_line1="Plot 42, Road No. 36, Jubilee Hills",
            city="Hyderabad",
            state="Telangana",
            pincode="500033",
            country="India"
        )
    
    settings_obj, _ = RestaurantSetting.objects.get_or_create(restaurant=restaurant)
    
    form = RestaurantForm(request.POST or None, request.FILES or None, instance=restaurant)
    settings_form = RestaurantSettingForm(request.POST or None, instance=settings_obj)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'save_profile' and form.is_valid():
            form.save()
            messages.success(request, "Restaurant corporate profile updated.")
            return redirect('restaurants:profile')
        elif action == 'save_settings' and settings_form.is_valid():
            settings_form.save()
            messages.success(request, "Operational settings updated.")
            return redirect('restaurants:profile')

    return render(request, 'restaurants/profile.html', {
        'restaurant': restaurant,
        'form': form,
        'settings_form': settings_form,
    })

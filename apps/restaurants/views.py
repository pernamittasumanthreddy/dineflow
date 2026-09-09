"""Restaurant Profile and Configuration Views."""
from django.shortcuts import render, redirect
from django.contrib import messages
from apps.restaurants.models import Restaurant, RestaurantSetting
from apps.restaurants.forms import RestaurantForm, RestaurantSettingForm
from apps.accounts.decorators import role_required

@role_required(['super_admin', 'owner'])
def restaurant_profile_view(request):
    """View and update restaurant corporate entity profile."""
    restaurant = Restaurant.objects.first()
    if not restaurant:
        restaurant = Restaurant.objects.create(
            name="Andhra Spice Kitchen & Grand Dine",
            slug="andhra-spice-kitchen",
            legal_entity_name="DineFlow Hospitality Private Limited",
            gstin="36AABCS1429B1Z8",
            fssai_number="10020042001234",
            email="contact@dineflow.internal",
            phone="+91 40 2334 5678",
            address_line1="Plot 42, Road No. 36, Jubilee Hills",
            city="Hyderabad",
            state="Telangana",
            pincode="500034",
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

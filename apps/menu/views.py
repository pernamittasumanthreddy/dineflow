"""Culinary Catalog and Recipe Management Views."""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from apps.menu.models import Category, MenuItem, MenuItemVariant, MenuItemAddon, RecipeItem
from apps.menu.forms import CategoryForm, MenuItemForm, MenuItemVariantForm, MenuItemAddonForm
from apps.accounts.decorators import module_permission_required

@login_required
def menu_catalog_view(request):
    """Interactive food catalog displaying categories and dishes."""
    categories = Category.objects.filter(is_active=True).prefetch_related('items')
    items = MenuItem.objects.filter(is_active=True).select_related('category')
    
    selected_cat_id = request.GET.get('category')
    search_q = request.GET.get('q')
    food_filter = request.GET.get('food_type')
    
    if selected_cat_id:
        items = items.filter(category_id=selected_cat_id)
    if search_q:
        items = items.filter(Q(name__icontains=search_q) | Q(code__icontains=search_q) | Q(description__icontains=search_q))
    if food_filter:
        items = items.filter(food_type=food_filter)

    return render(request, 'menu/catalog.html', {
        'categories': categories,
        'items': items,
        'selected_cat': selected_cat_id,
        'search_q': search_q,
        'food_filter': food_filter,
    })

@login_required
@module_permission_required('menu')
def menu_item_create_view(request):
    """Add a new culinary item to the menu."""
    form = MenuItemForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        item = form.save()
        messages.success(request, f"Menu item '{item.name}' added successfully.")
        return redirect('menu:catalog')
    return render(request, 'menu/item_form.html', {'form': form, 'title': 'Create Menu Item'})

@login_required
@module_permission_required('menu')
def menu_item_edit_view(request, item_id):
    """Edit menu item specifications, pricing, or availability."""
    item = get_object_or_404(MenuItem, id=item_id)
    form = MenuItemForm(request.POST or None, request.FILES or None, instance=item)
    variant_form = MenuItemVariantForm(request.POST or None)
    addon_form = MenuItemAddonForm(request.POST or None)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'save_item' and form.is_valid():
            form.save()
            messages.success(request, f"Item '{item.name}' updated.")
            return redirect('menu:item_edit', item_id=item.id)
        elif action == 'add_variant' and variant_form.is_valid():
            var = variant_form.save(commit=False)
            var.menu_item = item
            var.save()
            messages.success(request, f"Variant '{var.name}' added.")
            return redirect('menu:item_edit', item_id=item.id)
        elif action == 'add_addon' and addon_form.is_valid():
            addon = addon_form.save(commit=False)
            addon.menu_item = item
            addon.save()
            messages.success(request, f"Add-on '{addon.name}' added.")
            return redirect('menu:item_edit', item_id=item.id)

    return render(request, 'menu/item_edit.html', {
        'item': item,
        'form': form,
        'variant_form': variant_form,
        'addon_form': addon_form,
        'variants': item.variants.all(),
        'addons': item.addons.all(),
        'recipe_ingredients': item.recipe_ingredients.all(),
    })

@login_required
@module_permission_required('menu')
def menu_item_toggle_availability_view(request, item_id):
    """Quick 86 / toggle availability in kitchen/POS."""
    item = get_object_or_404(MenuItem, id=item_id)
    item.is_available = not item.is_available
    item.save(update_fields=['is_available'])
    messages.info(request, f"{item.name} is now {'Available' if item.is_available else 'Unavailable (86ed)'}.")
    return redirect(request.META.get('HTTP_REFERER') or 'menu:catalog')

@login_required
@module_permission_required('menu')
def category_list_view(request):
    """Manage menu categories."""
    categories = Category.objects.all()
    form = CategoryForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        cat = form.save()
        messages.success(request, f"Category '{cat.name}' created.")
        return redirect('menu:category_list')
    return render(request, 'menu/category_list.html', {
        'categories': categories,
        'form': form,
    })

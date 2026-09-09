"""Inventory Dashboard, Stock Movements, and Waste Adjustment Views."""
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.inventory.models import Ingredient, IngredientCategory, StockMovement, MovementType
from apps.accounts.decorators import module_permission_required

@login_required
@module_permission_required('inventory')
def stock_list_view(request):
    """Real-time inventory levels, low stock alerts, and valuation."""
    branch = request.user.branch
    ingredients = Ingredient.objects.filter(is_active=True).select_related('category', 'branch')
    
    if branch:
        ingredients = ingredients.filter(branch=branch)
        
    category_id = request.GET.get('category')
    filter_low_stock = request.GET.get('low_stock')
    
    if category_id:
        ingredients = ingredients.filter(category_id=category_id)
    if filter_low_stock == '1':
        ingredients = [ing for ing in ingredients if ing.is_low_stock]

    categories = IngredientCategory.objects.all()
    total_val = sum(i.stock_value for i in ingredients)
    low_stock_count = sum(1 for i in ingredients if i.is_low_stock)

    return render(request, 'inventory/stock_list.html', {
        'ingredients': ingredients,
        'categories': categories,
        'total_valuation': total_val,
        'low_stock_count': low_stock_count,
        'selected_category': category_id,
    })

@login_required
@module_permission_required('inventory')
def stock_adjust_view(request, ingredient_id):
    """Adjust physical stock count or record kitchen waste/spoilage."""
    ingredient = get_object_or_404(Ingredient, id=ingredient_id)
    
    if request.method == 'POST':
        movement_type = request.POST.get('movement_type', MovementType.WASTE_SPOILAGE)
        quantity_str = request.POST.get('quantity', '0.000')
        qty_delta = Decimal(quantity_str)
        reason = request.POST.get('notes', '').strip()
        
        old_stock = ingredient.current_stock
        
        if movement_type == MovementType.AUDIT_ADJUSTMENT:
            # Absolute new stock target
            new_stock = qty_delta
            delta = new_stock - old_stock
        else:
            # Delta deduction (waste is negative)
            delta = -abs(qty_delta)
            new_stock = max(Decimal('0.000'), old_stock + delta)

        ingredient.current_stock = new_stock
        ingredient.save(update_fields=['current_stock'])

        StockMovement.objects.create(
            ingredient=ingredient,
            movement_type=movement_type,
            quantity=delta,
            stock_before=old_stock,
            stock_after=new_stock,
            reference_id=f"ADJ-{request.user.username.upper()}",
            recorded_by=request.user,
            notes=reason
        )

        messages.success(request, f"Stock updated for {ingredient.name}. New level: {new_stock} {ingredient.unit}")
        return redirect('inventory:stock_list')

    return render(request, 'inventory/adjust_form.html', {
        'ingredient': ingredient,
        'movement_types': [MovementType.WASTE_SPOILAGE, MovementType.AUDIT_ADJUSTMENT]
    })

@login_required
@module_permission_required('inventory')
def stock_movements_view(request):
    """Audit ledger of all stock intake, consumption, waste, and adjustments."""
    branch = request.user.branch
    movements = StockMovement.objects.all().select_related('ingredient__category', 'recorded_by')
    
    if branch:
        movements = movements.filter(ingredient__branch=branch)
        
    movement_type = request.GET.get('type')
    if movement_type:
        movements = movements.filter(movement_type=movement_type)

    movements = movements.order_by('-created_at')[:100]

    return render(request, 'inventory/movements.html', {
        'movements': movements,
        'movement_types': MovementType.choices,
        'selected_type': movement_type,
    })

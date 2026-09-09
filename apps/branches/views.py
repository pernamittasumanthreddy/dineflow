"""Branch Management and Switcher Views."""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from apps.branches.models import Branch
from apps.branches.forms import BranchForm
from apps.restaurants.models import Restaurant
from apps.accounts.decorators import role_required

@role_required(['super_admin', 'owner', 'manager'])
def branch_list_view(request):
    """View all operational outlets / branches."""
    branches = Branch.objects.all().select_related('manager', 'restaurant')
    return render(request, 'branches/branch_list.html', {'branches': branches})

@role_required(['super_admin', 'owner'])
def branch_create_view(request):
    """Create a new restaurant branch."""
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
    form = BranchForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        branch = form.save(commit=False)
        branch.restaurant = restaurant
        branch.save()
        messages.success(request, f"Branch '{branch.name}' created successfully.")
        return redirect('branches:list')
    return render(request, 'branches/branch_form.html', {'form': form, 'title': 'Add New Branch'})

@role_required(['super_admin', 'owner'])
def branch_edit_view(request, branch_id):
    """Edit branch details."""
    branch = get_object_or_404(Branch, id=branch_id)
    form = BranchForm(request.POST or None, instance=branch)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, f"Branch '{branch.name}' updated.")
        return redirect('branches:list')
    return render(request, 'branches/branch_form.html', {'form': form, 'title': f'Edit Branch: {branch.name}'})

@role_required(['super_admin', 'owner', 'manager', 'cashier', 'waiter'])
def switch_branch_view(request, branch_id):
    """Switch user's active branch context in session."""
    branch = get_object_or_404(Branch, id=branch_id)
    request.session['active_branch_id'] = branch.id
    request.session['active_branch_name'] = branch.name
    # Update userprofile branch name if present
    if hasattr(request.user, 'userprofile'):
        request.user.userprofile.branch = branch.name
        request.user.userprofile.save(update_fields=['branch'])
    messages.info(request, f"Active outlet switched to {branch.name}.")
    next_url = request.META.get('HTTP_REFERER') or '/dashboard/owner/'
    return redirect(next_url)

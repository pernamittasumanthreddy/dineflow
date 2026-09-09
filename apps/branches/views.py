"""Branch Management and Switcher Views."""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.branches.models import Branch
from apps.branches.forms import BranchForm
from apps.restaurants.models import Restaurant
from apps.accounts.decorators import role_required, module_permission_required

@login_required
def branch_list_view(request):
    """View all operational outlets / branches."""
    branches = Branch.objects.all().select_related('manager', 'restaurant')
    return render(request, 'branches/branch_list.html', {'branches': branches})

@login_required
@module_permission_required('settings')
def branch_create_view(request):
    """Create a new restaurant branch."""
    restaurant = Restaurant.objects.first()
    form = BranchForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        branch = form.save(commit=False)
        branch.restaurant = restaurant
        branch.save()
        messages.success(request, f"Branch '{branch.name}' created successfully.")
        return redirect('branches:list')
    return render(request, 'branches/branch_form.html', {'form': form, 'title': 'Add New Branch'})

@login_required
@module_permission_required('settings')
def branch_edit_view(request, branch_id):
    """Edit branch details."""
    branch = get_object_or_404(Branch, id=branch_id)
    form = BranchForm(request.POST or None, instance=branch)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, f"Branch '{branch.name}' updated.")
        return redirect('branches:list')
    return render(request, 'branches/branch_form.html', {'form': form, 'title': f'Edit Branch: {branch.name}'})

@login_required
def switch_branch_view(request, branch_id):
    """Switch user's active branch context in session."""
    branch = get_object_or_404(Branch, id=branch_id)
    user = request.user
    user.branch = branch
    user.save(update_fields=['branch'])
    request.session['active_branch_id'] = branch.id
    messages.info(request, f"Active outlet switched to {branch.name}.")
    next_url = request.META.get('HTTP_REFERER') or 'core:dashboard'
    return redirect(next_url)

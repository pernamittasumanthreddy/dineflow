"""Floor Plan, Table Grid, and Occupancy Views."""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.tables.models import FloorSection, RestaurantTable, TableStatus
from apps.tables.forms import FloorSectionForm, RestaurantTableForm
from apps.accounts.decorators import module_permission_required

@login_required
def floor_plan_view(request):
    """Visual interactive floor layout showing all tables with status."""
    branch = request.user.branch
    tables = RestaurantTable.objects.filter(is_active=True).select_related('section', 'current_order')
    sections = FloorSection.objects.filter(is_active=True)
    
    if branch:
        tables = tables.filter(branch=branch)
        sections = sections.filter(branch=branch)
        
    selected_section_id = request.GET.get('section')
    if selected_section_id:
        tables = tables.filter(section_id=selected_section_id)

    status_counts = {
        'total': tables.count(),
        'available': tables.filter(status=TableStatus.AVAILABLE).count(),
        'occupied': tables.filter(status=TableStatus.OCCUPIED).count(),
        'reserved': tables.filter(status=TableStatus.RESERVED).count(),
        'cleaning': tables.filter(status=TableStatus.CLEANING).count(),
    }

    return render(request, 'tables/floor_plan.html', {
        'tables': tables,
        'sections': sections,
        'selected_section': selected_section_id,
        'status_counts': status_counts,
        'statuses': TableStatus.choices,
    })

@login_required
def table_toggle_status_view(request, table_id):
    """Change table state (e.g., mark as Cleaning or Available)."""
    table = get_object_or_404(RestaurantTable, id=table_id)
    new_status = request.POST.get('status')
    if new_status in TableStatus.values:
        table.status = new_status
        if new_status == TableStatus.AVAILABLE:
            table.current_order = None
        table.save(update_fields=['status', 'current_order'])
        messages.success(request, f"Table {table.table_number} marked as {table.get_status_display()}.")
    return redirect(request.META.get('HTTP_REFERER') or 'tables:floor_plan')

@login_required
@module_permission_required('tables')
def table_create_view(request):
    """Register a new table in the branch."""
    form = RestaurantTableForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        table = form.save(commit=False)
        table.branch = request.user.branch or FloorSection.objects.first().branch
        table.save()
        messages.success(request, f"Table {table.table_number} created.")
        return redirect('tables:floor_plan')
    return render(request, 'tables/table_form.html', {'form': form, 'title': 'Add Table'})

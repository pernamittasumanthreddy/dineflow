"""System Audit Trail Log Views."""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.audit.models import AuditLog, AuditAction
from apps.accounts.decorators import module_permission_required

@login_required
@module_permission_required('audit')
def audit_log_list_view(request):
    """Global system audit log viewer."""
    logs = AuditLog.objects.all().select_related('actor')
    
    action_filter = request.GET.get('action')
    module_filter = request.GET.get('module')
    
    if action_filter:
        logs = logs.filter(action=action_filter)
    if module_filter:
        logs = logs.filter(module_name=module_filter)

    logs = logs.order_by('-timestamp')[:100]

    return render(request, 'audit/log_list.html', {
        'logs': logs,
        'action_filter': action_filter,
        'module_filter': module_filter,
        'actions': AuditAction.choices,
    })

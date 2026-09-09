"""Audit Trail Logging and Diff Recording Services."""
from apps.audit.models import AuditLog, AuditAction

def log_audit_action(actor, action, module_name, object_id, object_repr, old_values=None, new_values=None, ip_address=None):
    """
    Creates an immutable audit log entry.
    """
    log = AuditLog.objects.create(
        actor=actor,
        action=action,
        module_name=module_name,
        object_id=str(object_id),
        object_repr=str(object_repr),
        old_values=old_values or {},
        new_values=new_values or {},
        ip_address=ip_address
    )
    return log

def get_audit_trail_for_object(module_name, object_id):
    """
    Returns complete chronological audit history for a specific entity.
    """
    return list(AuditLog.objects.filter(module_name=module_name, object_id=str(object_id)).order_by('-timestamp'))

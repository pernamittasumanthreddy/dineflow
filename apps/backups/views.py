"""Database Snapshot and Data Backup Manager Views."""
import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import FileResponse, Http404
from apps.backups.models import DatabaseBackupRecord, create_database_backup
from apps.accounts.decorators import role_required
from apps.accounts.models import RoleChoices

@login_required
@role_required(RoleChoices.SUPER_ADMIN, RoleChoices.RESTAURANT_OWNER)
def backup_list_view(request):
    """View and trigger database backup snapshots."""
    backups = DatabaseBackupRecord.objects.all()
    return render(request, 'backups/backup_list.html', {'backups': backups})

@login_required
@role_required(RoleChoices.SUPER_ADMIN, RoleChoices.RESTAURANT_OWNER)
def backup_create_view(request):
    """Trigger creation of a fresh JSON database snapshot."""
    try:
        record = create_database_backup()
        messages.success(request, f"Backup {record.filename} created ({record.file_size_bytes} bytes).")
    except Exception as e:
        messages.error(request, f"Backup failed: {str(e)}")
    return redirect('backups:list')

@login_required
@role_required(RoleChoices.SUPER_ADMIN, RoleChoices.RESTAURANT_OWNER)
def backup_download_view(request, backup_id):
    """Download the JSON backup fixture file."""
    record = get_object_or_404(DatabaseBackupRecord, id=backup_id)
    if not os.path.exists(record.file_path):
        raise Http404("Backup file not found on disk.")
    return FileResponse(open(record.file_path, 'rb'), as_attachment=True, filename=record.filename)

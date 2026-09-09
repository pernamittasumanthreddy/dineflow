"""Local Database Snapshot and Data Fixture Backup Utility."""
import os
import subprocess
from datetime import datetime
from django.conf import settings
from django.core.management import call_command
from apps.core.models import TimeStampedModel
from django.db import models

class DatabaseBackupRecord(TimeStampedModel):
    """Log of created database snapshots."""
    filename = models.CharField(max_length=150)
    file_path = models.CharField(max_length=255)
    file_size_bytes = models.BigIntegerField(default=0)
    status = models.CharField(max_length=20, default='SUCCESS')

    class Meta:
        verbose_name = 'Database Backup Record'
        verbose_name_plural = 'Database Backup Records'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.filename} ({self.file_size_bytes} bytes)"

def create_database_backup():
    """Dumps all database fixtures into a compressed JSON backup archive."""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"dineflow_backup_{timestamp}.json"
    file_path = os.path.join(settings.BACKUPS_DIR, filename)

    with open(file_path, 'w', encoding='utf-8') as f:
        call_command('dumpdata', exclude=['contenttypes', 'auth.permission'], stdout=f)

    file_size = os.path.getsize(file_path) if os.path.exists(file_path) else 0

    record = DatabaseBackupRecord.objects.create(
        filename=filename,
        file_path=file_path,
        file_size_bytes=file_size,
        status='SUCCESS'
    )
    return record

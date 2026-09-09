"""Automated Database Snapshot Command."""
from django.core.management.base import BaseCommand
from apps.backups.models import create_database_backup

class Command(BaseCommand):
    help = 'Executes a local database snapshot and registers a DatabaseBackupRecord.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Initiating DineFlow local database backup..."))
        try:
            record = create_database_backup()
            size_kb = round(record.file_size_bytes / 1024, 2)
            self.stdout.write(self.style.SUCCESS(f"[OK] Database snapshot created: {record.filename} ({size_kb} KB)"))
            self.stdout.write(self.style.SUCCESS(f"[OK] Location: {record.file_path}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"[FAIL] Backup failed: {e}"))

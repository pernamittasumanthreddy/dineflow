"""Comprehensive Test Suite for Database Backup Snapshots and Management Commands."""
import os
from io import StringIO
from django.test import TestCase
from django.core.management import call_command
from apps.backups.models import DatabaseBackupRecord, create_database_backup

class DatabaseBackupTestCase(TestCase):
    def test_create_database_backup_function(self):
        """Test create_database_backup generates a valid json dump file and record."""
        record = create_database_backup()
        self.assertIsNotNone(record)
        self.assertEqual(record.status, 'SUCCESS')
        self.assertTrue(os.path.exists(record.file_path))
        self.assertGreater(record.file_size_bytes, 0)
        
        # Clean up created file
        if os.path.exists(record.file_path):
            os.remove(record.file_path)

    def test_backup_dineflow_command(self):
        """Test backup_dineflow management command outputs success message."""
        out = StringIO()
        call_command('backup_dineflow', stdout=out)
        output = out.getvalue()
        self.assertIn("DineFlow local database backup", output)
        self.assertIn("[OK] Database snapshot created", output)
        
        # Clean up created file
        record = DatabaseBackupRecord.objects.first()
        if record and os.path.exists(record.file_path):
            os.remove(record.file_path)

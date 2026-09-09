from django.test import TestCase

from apps.core.models import Branch, Restaurant
from services.backup_service import DatabaseBackupService


class SoftDeleteAndBackupTestCase(TestCase):
    def setUp(self):
        self.restaurant = Restaurant.objects.create(
            name='Soft Delete Test Rest',
            code='SD_TEST',
            email='sd@test.com',
            phone='9000011111'
        )
        self.branch = Branch.objects.create(
            restaurant=self.restaurant,
            name='Test Branch',
            code='TB01',
            city='Hyderabad',
            state='Telangana',
            pincode='500001',
            phone='9000011111',
            email='tb01@test.com'
        )

    def test_soft_delete_behavior(self):
        """Validates that soft_delete hides entity from default queryset while preserving in all_objects."""
        self.assertEqual(Branch.objects.filter(id=self.branch.id).count(), 1)

        self.branch.soft_delete()
        self.branch.refresh_from_db()

        self.assertTrue(self.branch.is_deleted)
        self.assertIsNotNone(self.branch.deleted_at)

        # Standard manager should hide it
        self.assertEqual(Branch.objects.filter(id=self.branch.id).count(), 0)

        # all_objects manager should include it
        self.assertEqual(Branch.all_objects.filter(id=self.branch.id).count(), 1)

        # Restore
        self.branch.restore()
        self.branch.refresh_from_db()
        self.assertFalse(self.branch.is_deleted)
        self.assertIsNone(self.branch.deleted_at)
        self.assertEqual(Branch.objects.filter(id=self.branch.id).count(), 1)

    def test_backup_service_creation_and_integrity(self):
        """Validates that backup service produces verifiable file and checksum record."""
        bk = DatabaseBackupService.create_backup(backup_type='FULL_SQLITE')
        self.assertIsNotNone(bk.backup_id)
        self.assertEqual(bk.status, 'COMPLETED')
        self.assertTrue(len(bk.checksum_sha256) == 64)  # SHA-256 length

        # Verify integrity
        is_valid = DatabaseBackupService.verify_backup_integrity(bk)
        self.assertTrue(is_valid)

        # Restore verification
        restored = DatabaseBackupService.restore_backup(bk)
        self.assertTrue(restored)
        bk.refresh_from_db()
        self.assertEqual(bk.restore_status, 'RESTORE_VERIFIED')

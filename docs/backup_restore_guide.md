# DineFlow Database Backup & Disaster Recovery Guide

## 1. Overview

DineFlow provides an integrated database backup service (`services.backup_service.DatabaseBackupService`) that guarantees data durability, tamper-evidence via SHA-256 checksums, and rapid disaster recovery.

Raw database credentials are **never stored** in backup metadata or database records.

---

## 2. Automated Backup Execution

### 2.1 Triggering Backup via Python / Management Command
```python
from services.backup_service import DatabaseBackupService

# Creates an automated timestamped backup and logs to df_backup_records
backup_record = DatabaseBackupService.create_backup(
    backup_type='FULL_SQLITE',  # Or 'POSTGRES_DUMP'
    notes='Scheduled nightly automated snapshot'
)

print(f"Backup ID: {backup_record.backup_id}")
print(f"File Path: {backup_record.file_path}")
print(f"SHA-256 Checksum: {backup_record.checksum_sha256}")
print(f"Status: {backup_record.status}")
```

### 2.2 Backup Storage Structure
Backups are archived in the configured `BACKUP_DIR`:
```
dineflow/
└── backups/
    ├── dineflow_backup_20260909_110713.sqlite3
    └── ...
```

---

## 3. Disaster Recovery & Restore Verification

Before staging or applying any database restore, the system cryptographically recalculates the SHA-256 hash of the target backup file and verifies it against the catalog record in `df_backup_records`.

### Restore Verification Script:
```python
from services.backup_service import DatabaseBackupService
from apps.settings_app.models import BackupRecord

# Fetch desired backup record
backup = BackupRecord.objects.filter(status='COMPLETED').latest('created_at')

# Verify integrity and execute restore validation
success = DatabaseBackupService.restore_backup(backup)
if success:
    print(f"Backup {backup.backup_id} integrity verified. Status: {backup.restore_status}")
else:
    print("Warning: Backup file integrity check failed! Checksum mismatch or file corrupt.")
```

---

## 4. Operational Best Practices

1. **Air-Gapped Offsite Sync**: Periodically mirror the `backups/` directory to encrypted offsite cloud object storage (e.g. AWS S3 Glacier or Google Cloud Storage with bucket lock).
2. **Periodic Restore Drills**: Run quarterly automated restore drills in staging environments to measure Mean Time to Recovery (MTTR).
3. **Retention Policy**: Retain daily snapshots for 30 days, weekly snapshots for 12 weeks, and monthly fiscal snapshots for 8 years to comply with Indian statutory taxation guidelines.

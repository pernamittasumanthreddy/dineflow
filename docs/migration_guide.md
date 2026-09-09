# DineFlow Database Migration Guide (SQLite to PostgreSQL)

This guide documents the procedures for deploying DineFlow from local development (SQLite) to production-ready enterprise PostgreSQL clusters.

## 1. Environment Configuration

DineFlow uses standard environment variables in `dineflow/settings.py` to seamlessly toggle between database backends without modifying source code:

### PostgreSQL Environment Variables (.env):
```env
DB_ENGINE=postgresql
DB_NAME=dineflow_prod
DB_USER=dineflow_admin
DB_PASSWORD=SecurePassword_Here_123!
DB_HOST=127.0.0.1
DB_PORT=5432
```

---

## 2. Step-by-Step Production Deployment Procedure

### Step 1: Provision Database & User in PostgreSQL
```sql
CREATE DATABASE dineflow_prod WITH ENCODING 'UTF8';
CREATE USER dineflow_admin WITH PASSWORD 'SecurePassword_Here_123!';
GRANT ALL PRIVILEGES ON DATABASE dineflow_prod TO dineflow_admin;
```

### Step 2: Run System Verifications
```powershell
python manage.py check --deploy
```

### Step 3: Apply Clean Migrations in PostgreSQL
```powershell
$env:DB_ENGINE="postgresql"
$env:DB_NAME="dineflow_prod"
$env:DB_USER="dineflow_admin"
$env:DB_PASSWORD="SecurePassword_Here_123!"

python manage.py migrate
```

### Step 4: Seed Initial Master & Statutory Data
```powershell
python scripts/seed_demo_data.py
```

### Step 5: Verify Schema & Foreign Key Constraints
```powershell
python manage.py test tests/
```

---

## 3. Safe Migration Safeguards

1. **Non-Destructive Migrations**: Never drop columns or truncate tables in a single migration step. Always deprecate, backfill, and remove in separate migration phases.
2. **Backward-Compatible Schema**: Ensure default values are provided for newly introduced columns on existing tables.
3. **Lock Minimization**: In PostgreSQL production environments, add indexes using `CONCURRENTLY` where tables exceed 100,000 rows.

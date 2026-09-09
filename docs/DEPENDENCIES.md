# DineFlow ERP - Dependency & Package Lock Documentation

This document outlines the complete dependency management architecture, manifests, lockfiles, and step-by-step installation instructions for **DineFlow Enterprise Restaurant ERP**.

---

## 1. Manifests & Lockfiles Summary

DineFlow enforces deterministic, reproducible builds by pairing every dependency manifest with an exact lockfile:

| Ecosystem | Manifest File | Lockfile | Purpose |
| :--- | :--- | :--- | :--- |
| **Python (Poetry)** | [`pyproject.toml`](file:///c:/Users/BABI/Desktop/dineflow/pyproject.toml) | [`poetry.lock`](file:///c:/Users/BABI/Desktop/dineflow/poetry.lock) | Core ERP Backend, REST APIs, ML Models, Database Migrations |
| **Python (Pip fallback)** | [`requirements.txt`](file:///c:/Users/BABI/Desktop/dineflow/requirements.txt) | *(Pinned in file)* | Containerized deployments, CI/CD runners |
| **Node.js / Frontend** | [`package.json`](file:///c:/Users/BABI/Desktop/dineflow/package.json) | [`package-lock.json`](file:///c:/Users/BABI/Desktop/dineflow/package-lock.json) | Frontend asset bundling, Tailwind CSS, Lucide icons |

---

## 2. System Requirements

- **Python**: `>= 3.12.0`
- **Node.js**: `>= 20.0.0` (with `npm >= 10.0.0`)
- **Poetry**: `>= 2.0.0` (optional, can also use `pip`)
- **Database Engine**: SQLite 3 (default for local dev) or PostgreSQL 15+ (production)

---

## 3. Installation Steps

### Option A: Using Poetry (Recommended)

1. **Install Poetry** (if not already installed):
   ```bash
   pip install poetry
   ```

2. **Install all dependencies from lockfile** (guarantees exact cryptographic match):
   ```bash
   poetry install
   ```

3. **Activate virtual environment**:
   ```bash
   poetry shell
   ```

---

### Option B: Using Standard Python Virtual Environment (`venv` + `pip`)

1. **Create and activate a virtual environment**:
   ```powershell
   # Windows PowerShell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

2. **Upgrade pip and install pinned requirements**:
   ```powershell
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

---

### Option C: Frontend Assets Installation

1. **Install frontend dependencies using exact lockfile**:
   ```bash
   npm ci
   ```
   *(Or `npm install` to update packages based on `package.json`)*

---

## 4. Primary Python Dependencies

### Core Framework & ORM
- **`Django >= 5.1, < 7.0`**: Central monolithic framework, ORM, RBAC auth, templates.
- **`djangorestframework >= 3.14.0`**: REST API serializers, viewsets, token handlers.
- **`djangorestframework-simplejwt >= 5.3.0`**: JSON Web Token (JWT) stateless auth.
- **`django-cors-headers >= 4.3.0`**: Cross-Origin Resource Sharing middleware.

### Business Logic, Documents & Invoicing
- **`reportlab >= 4.0.0`**: PDF generation for GST tax invoices and KOT print slips.
- **`openpyxl >= 3.1.0`**: Excel export/import for inventory audits and vendor ledgers.
- **`qrcode >= 7.4.0`**: UPI QR code generation on dining tables and POS bills.
- **`pillow >= 10.2.0`**: Restaurant logos, food menu image processing.

### Data Science, BI & Machine Learning
- **`pandas >= 2.2.0`**: Analytics time-series aggregation and sales reporting.
- **`numpy >= 1.26.0`**: Mathematical matrix calculations for kitchen forecasting.
- **`scikit-learn >= 1.4.0`**: Menu demand forecasting and customer churn models.
- **`xgboost >= 2.0.0`**: Gradient-boosted peak dining hour prediction models.

### Task Scheduling & Utilities
- **`apscheduler >= 3.10.0`**: Background crons for daily closing snapshots & stock alerts.
- **`python-dotenv >= 1.0.0`**: Environment configuration loader.
- **`faker >= 24.0.0`**: Enterprise test data and realistic seeding generator.

### Development, QA & Code Quality
- **`ruff >= 0.4.0`**: Ultra-fast linting and static code analysis.
- **`pytest >= 8.0.0`**: Test suite runner.
- **`pytest-django >= 4.8.0`**: Django fixtures and DB test helpers.
- **`pytest-cov >= 5.0.0`**: Test coverage reporting.

---

## 5. Lockfile Maintenance

To update or regenerate lockfiles after adding a new dependency:

```bash
# Update Python Poetry lockfile
poetry lock --no-update

# Update Node.js package-lock.json
npm install --package-lock-only
```

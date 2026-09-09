# DineFlow — Enterprise Restaurant ERP & Database Architecture

[![Django](https://img.shields.io/badge/Django-6.1-green.svg)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Database](https://img.shields.io/badge/Database-PostgreSQL%20%2F%20SQLite-orange.svg)]()
[![Code Style](https://img.shields.io/badge/Code%20Style-Ruff-000000.svg)](https://astral.sh/ruff)

DineFlow is a production-grade, multi-tenant Restaurant ERP & Management System engineered with Django ORM. It provides complete enterprise data modeling, relational constraints, concurrency-safe transactions, and Indian restaurant workflows across 24 dedicated domain applications.

---

## Key Features

- **Multi-Tenant Architecture**: Supports multiple restaurants, branches, and tiered permissions.
- **24 Normalized Domain Apps**: Covers Employees, Menu, Tables, Orders, Kitchen (KOT), Inventory, Purchases, Billing, Payments, Customers, Delivery, Offers, Loyalty, Reviews, Expenses, Taxes, Analytics, ML, Reports, Audit logs, and Backups.
- **Indian Localization**: Dual GST calculation (2.5% CGST + 2.5% SGST for intra-state, 5.0% IGST for inter-state), dynamic UPI B2C payment QR codes (`upi://pay`), itemized round-off adjustments, and authentic Indian culinary datasets.
- **Transactional Integrity**: Concurrency-safe atomic invoice generation (`select_for_update()`), automatic Bill of Materials (BOM) recipe inventory deductions upon KOT preparation, and immutable audit ledgers.
- **Zero-Lint Quality**: 100% compliant with PEP 8 and Ruff guidelines, with 0 errors across all 184 codebase files.

---

## Tech Stack

- **Framework**: Django 6.1 (Python 3.12)
- **Database Support**: SQLite (Local Dev / Offline POS) & PostgreSQL (Production)
- **ORM & Integrity**: CheckConstraints, UniqueConstraints, Foreign Key Protections (`PROTECT`/`CASCADE`/`SET_NULL`), and Composite Query Indexes
- **Testing**: Django Test Framework (16 comprehensive transactional & constraint test cases)
- **Code Standards**: Ruff & PEP 8

---

## Domain Architecture Overview

```
apps/
├── core/           # Tenant root (Restaurant), Multi-branch, Custom User, RBAC Roles
├── employees/      # Staff profiles, Departments, Designations, Shifts, Payroll
├── menu/           # Categories, Menu Items, Variants, Addons, Recipe BOM Ingredients
├── tables/         # Sections (AC, Family, Terrace), Tables, Seating Constraints, Reservations
├── orders/         # Dine-in, Takeaway, Delivery, Order Items, Order Discounts, Taxes
├── kitchen/        # Kitchen Stations, KOTs (Kitchen Order Tickets), Station Routing
├── inventory/      # Stock levels, Batches, Stock Movements (Ledger), Adjustments, Waste
├── suppliers/      # Supplier registry, Contacts, Ratings
├── purchases/      # Purchase Orders (PO), Goods Receipt Notes (GRN), Purchase Inwarding
├── billing/        # Invoices, Sequential Numbering, GST splits, Round-off, B2C UPI QR
├── payments/       # Cash, UPI, Card transactions, Refunds, Reconciliations
├── customers/      # Customer directory, Addresses, Dietary Preferences
├── delivery/       # Delivery orders, Delivery rider assignments, Status tracking
├── offers/         # Offers, Promo coupons, Branch & menu scoping
├── loyalty/        # Customer tiers (Bronze/Silver/Gold/Platinum), Points ledger, Rewards
├── reviews/        # Ratings (Food, Service, Ambiance 1-5), Moderation
├── expenses/       # Branch operating expense categories, Approvals
├── taxes/          # Tax categories, HSN/SAC codes, CGST/SGST/IGST rules
├── notifications/  # Notification center, Channel preferences
├── analytics/      # Daily/Monthly sales snapshots, Demand forecasting aggregates
├── ml/             # ML dataset registries, Training runs, Demand predictions
├── reports/        # Custom report definitions, Scheduled exports
├── audit/          # Change Data Capture (CDC) diffs, Security event logging
└── settings_app/   # Dynamic system configs, Automated checksummed backups
```

---

## Getting Started

### 1. Clone & Setup Environment

```bash
git clone https://github.com/pernamittasumanthreddy/dineflow.git
cd dineflow

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate   # On Windows
source venv/bin/activate # On Linux/macOS

# Install dependencies
pip install -r requirements.txt # or install Django
```

### 2. Apply Migrations & Seed Demo Data

```bash
# Apply schema migrations
python manage.py migrate

# Seed realistic multi-restaurant Indian demo dataset
python scripts/seed_demo_data.py
```

### 3. Run Automated Tests

```bash
python manage.py test tests
```

### 4. Start the Development Server

```bash
python manage.py runserver
```
Visit **[http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)** to explore the interactive database portal.

**Default Super Admin Credentials**:
- **Email**: `admin@dineflow.com`
- **Password**: `AdminPassword@123`

---

## Technical Documentation

Detailed architectural reports are available in the [`docs/`](docs/) directory:
- [Database Architecture Specification](docs/database_architecture.md)
- [Mermaid Entity-Relationship (ER) Diagram](docs/er_diagram.md)
- [Model Relationships & Foreign Key Policies](docs/model_relationships.md)
- [Data Dictionary](docs/data_dictionary.md)
- [Database Indexing & Query Optimization Guide](docs/indexing_guide.md)
- [PostgreSQL Production Migration Guide](docs/migration_guide.md)
- [Backup & Disaster Recovery Guide](docs/backup_restore_guide.md)

---

## License

This project is licensed under the MIT License.

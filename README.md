# DineFlow — Enterprise Indian Restaurant ERP & Management System

[![Django](https://img.shields.io/badge/Django-5.2+-1E7A35?style=flat&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Database](https://img.shields.io/badge/Database-PostgreSQL%20%2F%20SQLite-orange.svg)]()
[![Code Style](https://img.shields.io/badge/Code%20Style-Ruff-000000.svg)](https://astral.sh/ruff)
[![Design](https://img.shields.io/badge/Palette-Zero--Blue%20Warm%20Spice-C24312?style=flat)](static/css/dineflow-tokens.css)

**DineFlow** is a comprehensive, multi-outlet, omnichannel enterprise ERP & Operating System crafted specifically for Indian hospitality chains, fine-dining restaurants, quick-service restaurants (QSRs), and cloud kitchens.

---

## 🎨 Zero-Blue Luxury Indian Warm Aesthetic

DineFlow adheres strictly to a **Zero-Blue** warm Indian hospitality color system:
* **Deep Charcoal** (`#1E1E24`): Primary dark backgrounds, headers, and text
* **Warm Cream** (`#FAF8F5`): Canvas surfaces and soft cards
* **Spice Terracotta** (`#C24312`): Primary brand accent, interactive buttons, badges
* **Saffron Amber** (`#E67E22`): Secondary warnings, pending states, highlights
* **Crimson Maroon** (`#7A1A24`): Heritage headers, urgent alerts, destructive actions
* **Cardamom Gold** (`#D4AF37`): Premium highlights, loyalty badges, VIP tiers
* **Emerald Green** (`#1E7A35`): Pure-Veg badges, active statuses, settled payments, tax green

---

## 👑 10 Dedicated Role Dashboards & Instant Role Switcher

Switch between any role at any time via the top navbar **Role Switcher** or the dedicated routes:

| Role | Route | Key Purpose |
| :--- | :--- | :--- |
| **Super Admin** | `/dashboard/super-admin/` | Multi-tenant SaaS metrics, system health, server loads, tenant billing |
| **Restaurant Owner** | `/dashboard/owner/` | Executive P&L, multi-branch revenue comparison, top sellers, live margins |
| **Store Manager** | `/dashboard/manager/` | Daily sales, table occupancy %, active staff counts, live operational alerts |
| **Kitchen Display / Chef** | `/dashboard/kitchen/` | KDS station load, pending KOT tickets, prep time SLA countdowns |
| **Captain / Waiter** | `/dashboard/waiter/` | Assigned tables, live order status, active KOTs, quick bill request |
| **Cashier** | `/dashboard/cashier/` | POS quick-launch, unbilled KOTs, shift cash drawer balance, payment settlement |
| **Inventory Manager** | `/dashboard/inventory/` | Critical stock alerts, expiry tracking, pending POs, ingredient variance |
| **HR / Payroll Manager** | `/dashboard/hr/` | On-duty staff, biometric attendance, shift rosters, Indian payroll (PF/ESI/TDS) |
| **Customer / Guest Portal** | `/dashboard/customer/` | Loyalty points ledger, tiered rewards (Silver/Gold/Platinum), order history |
| **Data & BI Analyst** | `/dashboard/analytics/` | Revenue forecasts, footfall heatmaps, menu item profitability matrix |

---

## 🚀 35+ Integrated Operational Modules

### 1. Point of Sale (POS) & Billing
* **POS Terminal** (`/pos/`): Fast-key menu grid, category tabs, diet filters (Veg/Non-Veg/Vegan/Jain), modifiers, split payments (Cash, UPI, Card), dynamic UPI QR code generator, and 80mm thermal / A4 GST invoice printing.
* **GST Split**: Automatic calculation of CGST (2.5%) + SGST (2.5%) or IGST (5%), Service Charge (optional 5%), and Rounding.
* **Invoices & Settlements** (`/billing/invoices/`): Comprehensive invoice register with reprint, settlement mode filters, and cancellation audit.
* **Day-End Z-Report** (`/billing/z-report/`): Cash drawer reconciliations, card settlements, UPI batch totals, and tax summary for daily closing.

### 2. Kitchen Display System (KDS) & Order Routing
* **KDS Live Kanban** (`/kds/`): Station filters (Tandoor, Curry & Gravy, South Indian / Dosa, Chinese / Pan-Asian, Beverages & Desserts), real-time prep timers with color warnings (Normal 🟢, Delayed 🟡, Overdue 🔴), bump item/order actions.
* **Live Orders Engine** (`/orders/live/`): Unified aggregator combining Dine-in, Zomato, Swiggy, Takeaway, and Direct Web orders.

### 3. Table & Floor Plan Management
* **Interactive Floor Plan** (`/tables/`): Visual table grid with live states (Available, Occupied, Reserved, Billed, Cleaning), VIP AC dining, Garden lawn, Rooftop, and Family sections.
* **Table Reservations** (`/tables/reservations/`): Guest booking calendar with SMS confirmation and advance deposit management.

### 4. Menu Engineering & Recipe Costing
* **Menu Master** (`/menu/`): Multi-price tiers, portion sizes, add-on groups, allergens, and dietary tagging.
* **Recipe Costing & BOM**: Ingredient-level cost breakdown, gross margin calculations, and automatic inventory depletion on KOT firing.

---

## 🏛️ Enterprise Database Architecture (Part 3)

- **Multi-Tenant Architecture**: Supports multiple restaurants, branches, and tiered permissions.
- **24 Normalized Domain Apps**: Employees, Menu, Tables, Orders, Kitchen (KOT), Inventory, Purchases, Billing, Payments, Customers, Delivery, Offers, Loyalty, Reviews, Expenses, Taxes, Analytics, ML, Reports, Audit logs, and Backups.
- **Indian Regulatory Localization**: Dual GST calculation (2.5% CGST + 2.5% SGST for intra-state, 5.0% IGST for inter-state), dynamic UPI B2C payment QR codes (`upi://pay`), itemized round-off adjustments, and authentic Indian culinary datasets.
- **Transactional Integrity**: Concurrency-safe atomic invoice generation (`select_for_update()`), automatic Bill of Materials (BOM) recipe inventory deductions upon KOT preparation, and immutable audit ledgers.
- **Zero-Lint Quality**: 100% compliant with PEP 8 and Ruff guidelines, with 0 errors across the codebase.

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

## ⚡ Quick Start Guide

### 1. Requirements
* Python 3.10+
* Django 5.2+

### 2. Setup Environment & Install Dependencies
```bash
git clone https://github.com/pernamittasumanthreddy/dineflow.git
cd dineflow

# Activate virtual environment
.venv\Scripts\activate   # On Windows
source .venv/bin/activate # On Linux/macOS
```

### 3. Apply Migrations & Seed Demo Data
```bash
# Apply schema migrations
python manage.py migrate

# Seed realistic multi-restaurant Indian demo dataset
python scripts/seed_demo_data.py
```

### 4. Run Automated Test Suite
```bash
python manage.py test tests
```

### 5. Start Development Server
```bash
python manage.py runserver
```
* **Landing Page & Dashboards**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
* **Admin Portal**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
  * **Super Admin**: `admin@dineflow.com` | `AdminPassword@123`

---

## 📚 Technical Documentation

Detailed architectural reports are available in the [`docs/`](docs/) directory:
- [Database Architecture Specification](docs/database_architecture.md)
- [Mermaid Entity-Relationship (ER) Diagram](docs/er_diagram.md)
- [Model Relationships & Foreign Key Policies](docs/model_relationships.md)
- [Data Dictionary](docs/data_dictionary.md)
- [Database Indexing & Query Optimization Guide](docs/indexing_guide.md)
- [PostgreSQL Production Migration Guide](docs/migration_guide.md)
- [Backup & Disaster Recovery Guide](docs/backup_restore_guide.md)

---

## 📄 License
© 2026 DineFlow Technologies Pvt. Ltd. All rights reserved.

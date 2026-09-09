# DineFlow — Indian Restaurant ERP & Cloud Kitchen Operating System

[![Django](https://img.shields.io/badge/Django-5.2+-1E7A35?style=flat&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Tests](https://img.shields.io/badge/Pytest-9%2F9%20Passing-1E7A35?style=flat&logo=pytest&logoColor=white)](file:///c:/Users/lenovo/Downloads/Elevateiq/DineFlow/tests/test_views.py)
[![Design](https://img.shields.io/badge/Palette-Zero--Blue%20Warm%20Spice-C24312?style=flat)](file:///c:/Users/lenovo/Downloads/Elevateiq/DineFlow/static/css/dineflow-tokens.css)

**DineFlow** is a comprehensive, multi-outlet, omnichannel enterprise ERP crafted specifically for Indian hospitality chains, fine-dining restaurants, quick-service restaurants (QSRs), and cloud kitchens.

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
* **Menu Master** (`/menu/`): Searchable menu items with FSSAI calorie counts, spice levels, allergens, and dietary badges.
* **Category Master** (`/menu/categories/`): Course ordering, tax slab mapping, printer routing.
* **Recipe Costing & Yield** (`/menu/recipe-costing/`): Ingredient-level breakdown, standard food cost % vs. actual, and portion margin calculators.

### 5. Supply Chain, Inventory & Procurement
* **Stock Ledger** (`/inventory/`): Real-time ingredient balance, min reorder levels, unit conversions (kg, g, L, ml, pcs).
* **Purchase Orders & GRN** (`/inventory/purchase-orders/`): Vendor POs with Goods Received Notes (GRN) matching.
* **Wastage & Spoilage Log** (`/inventory/waste-log/`): Kitchen prep loss and expiry logging with reason tracking.
* **Supplier Directory** (`/suppliers/`): Verified vendor records with GSTIN and payment terms.

### 6. Human Resources & Indian Payroll
* **Employee Directory** (`/hr/employees/`): Staff KYC, designation, role assignment, and bank details.
* **Attendance & Biometric Sync** (`/hr/attendance/`): Daily check-in/out logs, shift hours, overtime.
* **Shift Scheduling** (`/hr/shifts/`): Morning, Evening, and Split-shift rosters.
* **Statutory Payroll** (`/hr/payroll/`): Salary slips with Provident Fund (PF 12%), ESI (0.75%/3.25%), Professional Tax (PT), and TDS deductions.

### 7. CRM, Loyalty & Guest Experience
* **Customer Registry** (`/crm/customers/`): VIP tags, dietary preferences, anniversary/birthday triggers.
* **Loyalty Club** (`/crm/loyalty/`): Tiered points engine with redemption rules.
* **Promotions & Coupons** (`/crm/offers/`): Discount rules (Flat ₹, %, BOGO, Happy Hours).
* **Feedback & Reviews** (`/crm/feedback/`): Table QR rating logs with manager escalation.

### 8. Analytics, AI & Compliance
* **Business BI Suite** (`/analytics/bi/`): Pure HTML5 Canvas charts with zero external chart library bloat.
* **AI Demand Forecasting** (`/analytics/forecast/`): Day-wise footfall and raw ingredient usage predictions based on historical trends, weather, and festival calendar.
* **GST Compliance** (`/analytics/tax/` & `/tax/slabs/`): GSTR-1 and GSTR-3B export formatters, HSN tax slab management (0%, 5%, 12%, 18%).

### 9. Multi-Branch & Security Administration
* **Multi-Branch Control** (`/settings/branches/`): Headquarter view of Indiranagar, Koramangala, Connaught Place, and Bandra West outlets.
* **RBAC Engine** (`/settings/roles/`): Granular permission matrix for all 10 roles.
* **Audit Logs** (`/settings/audit/`): Immutable security trail of logins, price changes, discounts, and order cancellations.
* **Backup & Restore** (`/settings/backup/`): Snapshot generation, S3 sync, and point-in-time recovery.

---

## 💻 Tech Stack & Architecture

```
DineFlow Architecture
│
├── Public Website & Authentication
│   ├── Landing Page with Ambient Canvas Animation (Canvas Spice & Steam)
│   ├── Role-Aware Auth (Login, Register with GSTIN/FSSAI, OTP, Forgot Password)
│   └── Error Handler (404, 403, 500, Session Timeout)
│
├── Core & Middleware Layer
│   ├── Global Context Processor (Role switcher, branches, notifications)
│   ├── Custom Template Tags (inr_format, status_class, diet_badge)
│   └── Django 5.2 MVC
│
├── Presentation & Styling (Zero-Blue Design System)
│   ├── dineflow-tokens.css (CSS variables for warm Indian palette)
│   ├── dineflow-base.css (Global typography, layouts, grids)
│   ├── dineflow-components.css (Cards, badges, tables, modals, drawers, toasts)
│   ├── dineflow-pos.css & dineflow-kds.css (Specialized UI shells)
│   └── dineflow-landing.css (Hero animations, pricing cards, testimonials)
│
└── Reactive JavaScript Engines
    ├── landing-animation.js (Spice particles, steam physics)
    ├── dineflow-core.js (Role switcher, toasts, modal controllers)
    ├── pos-engine.js (Cart state machine, GST split, UPI QR renderer, thermal prints)
    ├── kds-engine.js (Live timer countdowns, station filter, bump system)
    ├── table-engine.js (Floor plan layout, status sync, reservations)
    ├── analytics-engine.js (Pure Canvas line, bar, donut charts)
    └── export-print.js (CSV/Excel client exporter, print formatter)
```

---

## ⚡ Quick Start Guide

### 1. Requirements
* Python 3.10+
* Django 5.0+

### 2. Run Locally
```bash
# Navigate to the project root
cd c:\Users\lenovo\Downloads\Elevateiq\DineFlow

# Apply migrations
python manage.py migrate

# Run test suite
pytest

# Start the development server
python manage.py runserver
```

Open your browser at [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

---

## 🧪 Test Suite

Run automated unit and integration tests:
```bash
pytest
```
Expected output:
```text
tests\test_views.py .........                                            [100%]
============================== 9 passed in 1.05s ==============================
```

---

## 📄 License
© 2026 DineFlow Technologies Pvt. Ltd. All rights reserved.

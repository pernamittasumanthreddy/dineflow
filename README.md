# DineFlow — Enterprise Restaurant ERP & Management System

> **A mission-critical, offline-first Restaurant Enterprise Resource Planning (ERP) platform built with Python 3.12, Django 5.1, Django ORM, Scikit-Learn AI, and a high-performance Vanilla CSS/JS design system tailored for Indian commercial food service enterprises.**

---

## 🌟 Key Highlights & Engineering Features

- **Modular Monolith Architecture**: High-cohesion, low-coupling design across **34 domain applications** running within a unified, atomic ACID database without microservice fragility.
- **10-Role Enterprise RBAC**: Granular role-based access control guarding endpoints and views (`SUPER_ADMIN`, `RESTAURANT_OWNER`, `MANAGER`, `KITCHEN_STAFF`, `WAITER`, `CASHIER`, `INVENTORY_MANAGER`, `HR`, `CUSTOMER`, `ANALYTICS_USER`).
- **100% Offline-First Design**: Zero external API dependencies. Includes offline transaction reference simulators (`TXN-UPI-*`, `TXN-POS-*`, `TXN-CASH-*`), local notification bus, and local machine learning inference.
- **Indian Statutory Localization**:
  - Currency: Indian Rupee (`₹`), formatted in Lakhs and Crores (e.g. `₹1,25,450.00`).
  - Timezone: `Asia/Kolkata` (IST, UTC+05:30).
  - Indian GST: Services Accounting Code **SAC 996331** (CGST 2.5% + SGST 2.5% for intra-state, IGST 5.0% for inter-state).
  - Mandatory Compliance: 15-character GSTIN, 14-digit FSSAI food safety licensing, and sequential tax invoices.
- **AI-Powered Demand & Procurement Forecasting**: Embedded Scikit-Learn `RandomForestRegressor` pipeline predicting 7-day forward covers, orders, gross revenue, and raw ingredient procurement needs.
- **Bill of Materials (BOM) Recipe Engine**: Automatic stock consumption and low-stock alerts based on dish recipes.
- **Indian Statutory Payroll**: Automated calculations for Basic (50%), HRA (25%), EPF (12% capped at ₹15,000), ESIC (0.75%), Professional Tax (₹200 slab), and Loss of Pay (LOP).
- **Hardware Peripherals Support**: ESC/POS thermal receipt formatting for 80mm and 58mm printers, plus Kitchen Order Tickets (KOT) with prep SLA tracking.
- **Luxury Obsidian Design System**: Custom dark-mode UI (`#090b10` deep obsidian, `#d97706` brushed gold, glassmorphism, responsive grid, Web Audio API kitchen chimes, live IST digital clock).

---

## 🏛️ System Architecture

```mermaid
graph TD
    subgraph Client Presentation Tier
        POS[Touch POS Terminal]
        KDS[Kitchen Display Stations]
        MGR[Manager Dashboard]
        STW[Steward Floor Plan]
    end

    subgraph Controller & Application Layer
        URL[Django URL Router]
        AUTH_MW[Session & RBAC Middleware]
        VIEWS[34 Domain App Controllers]
        UI[68 Domain Server Templates]
    end

    subgraph Enterprise Domain Services
        ORDER_ENG[Order State Machine]
        TAX_ENG[Indian GST SAC 9963 Engine]
        BOM_ENG[BOM Recipe Deduction]
        PAY_ENG[Indian Statutory Payroll]
        AI_ENG[Scikit-Learn Demand Forecaster]
        PRINT_ENG[ESC/POS Thermal Engine]
    end

    subgraph Persistence Tier
        DB[(SQLite WAL / PostgreSQL)]
        AUDIT[Immutable Security Audit Ledger]
        ML_MODEL[Serialized Joblib Pipeline]
    end

    Client Presentation Tier --> Controller & Application Layer
    Controller & Application Layer --> Enterprise Domain Services
    Enterprise Domain Services --> Persistence Tier
```

---

## 🚀 Quick Start Guide

### 1. Clone & Setup Environment
```bash
git clone <repository_url>
cd dineflow

# Create and activate virtual environment
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Initialize Database & Seed Master Data
```bash
# Apply schema migrations
python manage.py migrate

# Seed complete Indian restaurant enterprise dataset & train ML model
python manage.py seed_dineflow
```

### 3. Run Automated Tests
```bash
# Run the complete test suite (41 tests, 100% pass rate)
python manage.py test tests
```

### 4. Start Development Server
```bash
python manage.py runserver 0.0.0.0:8000
```
Visit `http://127.0.0.1:8000` in your web browser to access the DineFlow portal.

---

## 🔑 Default Credentials & Role Accounts

All seeded accounts share the default master password: **`DineFlow@2026`**

| Role | Username | Email | Primary Responsibilities |
| :--- | :--- | :--- | :--- |
| **Super Admin** | `admin` | `admin@dineflow.in` | Complete system administration, tenant configuration |
| **Restaurant Owner** | `owner` | `owner@royalnizam.in` | Executive oversight, multi-branch P&L reports |
| **General Manager** | `manager_hyd` | `manager.banjara@royalnizam.in` | Floor management, expense approvals, rosters |
| **Kitchen Staff / Chef**| `chef_vikram` | `chef.vikram@royalnizam.in` | Kitchen Display System (KDS), ticket bump actions |
| **Steward / Waiter** | `waiter_arjun` | `waiter.arjun@royalnizam.in` | Table reservations, dine-in ordering, guest service |
| **Cashier** | `cashier_priya` | `cashier.priya@royalnizam.in` | POS billing, GST tax invoices, cash drawer sessions |
| **Inventory Manager** | `inventory_kiran`| `inventory.kiran@royalnizam.in` | Stock movements, reorder alerts, purchase orders |
| **HR Manager** | `hr_pooja` | `hr.pooja@royalnizam.in` | Staff KYC, attendance, monthly Indian payroll runs |
| **Business Analyst** | `analytics_neha` | `analytics.neha@royalnizam.in` | BI dashboard, ML demand forecasts, turnover rates |
| **Customer / Guest** | `customer_rajesh`| `guest.rajesh@gmail.com` | Guest preferences, loyalty reward points balance |

---

## 🛠️ Management & Operational Commands

- **System Diagnostics**:
  ```bash
  python manage.py check_dineflow_health
  ```
- **Statutory Indian GST Return Export**:
  ```bash
  python manage.py export_gst_summary --month 9 --year 2026
  ```
- **Re-train ML Forecasting Model**:
  ```bash
  python manage.py seed_dineflow
  ```

---

## 📚 Technical Documentation

Comprehensive documentation is available in the [`docs/`](docs/) directory:
- [**Architecture & Topology**](docs/ARCHITECTURE.md): Modular monolith patterns, domain clusters, and offline-first principles.
- [**Permissions Matrix (RBAC)**](docs/PERMISSIONS_MATRIX.md): Detailed 10-role permission mappings across all 34 modules.
- [**Core Business Rules**](docs/BUSINESS_RULES.md): Statutory Indian GST rules, BOM recipe mechanics, table state machines, and payroll formulas.
- [**Database Schema & ERD**](docs/DATABASE_SCHEMA.md): Complete relational entity models, foreign keys, and dictionary.
- [**Security Hardening**](docs/SECURITY.md): Authentication, session controls, OWASP mitigation, and audit logging.
- [**Production Deployment**](docs/DEPLOYMENT.md): Nginx reverse proxy, Gunicorn systemd, SQLite WAL mode, and environment variables.

---

## 📄 License & Compliance

Developed for enterprise commercial food service operations. Compliant with **FSSAI Food Safety and Standards Act (2006)** and **Central Goods and Services Tax Act (2017)**.

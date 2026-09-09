# DineFlow ERP — System Architecture & Topology

## 1. Architectural Philosophy & Strategy

DineFlow is engineered as an enterprise-grade **Django Modular Monolith**. In commercial food service and hospitality environments, operational uptime, atomic data consistency, and offline resilience take precedence over distributed microservices.

### Why Modular Monolith Over Microservices?
1. **Atomic ACID Transactions**: Financial billing, inventory consumption, and order status transitions occur within unified database transactions without the fragility or latency of distributed two-phase commits (2PC) or Sagas.
2. **Zero External API Failure Points**: DineFlow is strictly offline-first. POS terminals, kitchen display systems (KDS), and cash drawer reconciliations continue running during internet outages or cloud infrastructure downtimes.
3. **Low Latency & High Throughput**: Sub-millisecond internal function calls replace HTTP/gRPC overhead between domain modules.
4. **Single-Command Operability**: The entire ERP boots locally with zero complex container orchestration required for standard restaurant branch deployments.

---

## 2. High-Level System Architecture

```mermaid
graph TD
    subgraph Client Tier
        POS[POS Touch Terminals]
        KDS[Kitchen Display Stations]
        MGR[Manager Dashboard]
        WAITER[Handheld Steward Terminals]
    end

    subgraph Presentation & Controller Layer
        URL[Django URL Dispatcher]
        MW[Security & Session Middleware]
        VIEWS[Domain Views & REST Endpoints]
        TMPL[Django Server-Rendered Templates + Static UI System]
    end

    subgraph Business Logic & Domain Services
        AUTH[RBAC & Auth Engine]
        ORDER_SM[Order State Machine]
        GST_ENG[Indian GST SAC 9963 Engine]
        BOM_ENG[BOM Recipe Consumption Engine]
        PAY_ENG[Indian Statutory Payroll Engine]
        ML_ENG[Scikit-Learn Demand Forecaster]
        ESC_ENG[ESC/POS Thermal Print Engine]
    end

    subgraph Data Persistence Tier
        DB[(SQLite WAL / PostgreSQL)]
        AUDIT[Immutable Audit Ledger]
        ML_STORE[Serialized Model Artifacts]
    end

    Client Tier -->|HTTP / Local LAN| Presentation & Controller Layer
    Presentation & Controller Layer --> Business Logic & Domain Services
    Business Logic & Domain Services --> Data Persistence Tier
```

---

## 3. Domain Functional Clusters (34 Domain Apps)

The 34 domain modules are organized into 6 functional clusters:

| Cluster | Apps | Core Responsibilities |
| :--- | :--- | :--- |
| **1. Foundation & Tenancy** | `core`, `restaurants`, `branches`, `accounts`, `settings_manager` | Base models, multi-branch tenancy, user authentication, 10-role RBAC, system settings. |
| **2. Culinary & Floor Operations** | `tables`, `menu`, `orders`, `kitchen`, `reservations`, `delivery` | Dining layout, interactive floor plan, POS order capture, KOT routing, KDS bump bar, table reservations, home delivery logistics. |
| **3. Revenue, Billing & Finance** | `tax`, `billing`, `payments`, `sales`, `expenses`, `refunds` | Indian GST (SAC 9963), statutory tax invoices, multi-method payment ledger, cash drawer float, operational expense vouchers, refunds. |
| **4. Supply Chain & Inventory** | `inventory`, `suppliers`, `purchases` | Raw material stock tracking (kg, L, pcs), minimum reorder alerts, supplier directory, purchase orders, BOM recipe deduction. |
| **5. Human Capital Management** | `employees`, `shifts`, `attendance`, `payroll` | Employee KYC (PAN/Aadhaar/UAN), shift roster scheduling, punch-in/out attendance, Indian statutory payroll (EPF, ESIC, PT). |
| **6. Intelligence, Marketing & Governance** | `customers`, `loyalty`, `offers`, `reviews`, `analytics`, `ml_prediction`, `reports`, `notifications`, `audit`, `backups` | CRM profiles, VIP loyalty points, coupons, guest reviews, executive BI snapshots, Scikit-Learn RandomForest demand predictions, audit trail, automated backups. |

---

## 4. Offline-First Principles

DineFlow adheres to strict offline-first operational rules:
1. **Mock Payment Simulator**: Internal transaction reference generation (`TXN-UPI-*`, `TXN-POS-*`, `TXN-CASH-*`) allows cashiers to settle bills without external payment gateway dependencies.
2. **Local Notification Bus**: System alerts, stock warnings, and order fires route through in-memory and local database notifications.
3. **Local Machine Learning**: Scikit-Learn regression models train and predict directly on the local machine using historical database records and synthetic distributions, saved as `.joblib` artifacts.

---

## 5. Indian Localization Engineering

- **Currency**: Indian Rupee (`₹`), formatted in Lakhs and Crores (e.g., `₹1,25,450.00`).
- **Timezone**: `Asia/Kolkata` (IST, UTC+05:30) used across all operational shift clocks, attendance registers, and transaction timestamps.
- **Taxation**: Indian Goods & Services Tax (GST) under Services Accounting Code **SAC 9963**:
  - Intra-state (Telangana -> Telangana): CGST 2.5% + SGST 2.5% (Total 5.0%).
  - Inter-state: IGST 5.0%.
- **Regulatory Compliance**: FSSAI 14-digit license numbers and 15-character GSTIN validation printed on all customer bills and statutory reports.

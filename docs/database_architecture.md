# DineFlow Database Architecture Document

## 1. Executive Summary

**DineFlow** is an enterprise-grade, multi-restaurant, multi-branch Restaurant ERP & Management System. This document specifies the comprehensive database architecture implemented in Django ORM with native support for both **SQLite (development/offline testing)** and **PostgreSQL (high-concurrency production deployments)**.

The database architecture is designed according to Third Normal Form (3NF) principles, preserving referential integrity, eliminating data anomalies, and supporting high-throughput restaurant point-of-sale (POS), kitchen display systems (KDS), inventory recipe consumption, and Indian GST tax compliance.

---

## 2. Core Architectural Tenets

### 2.1 Multi-Tenancy Architecture
- **Model**: Shared-Database, Row-Level Scoped Multi-Tenancy.
- **Tenant Hierarchy**:
  1. `df_restaurants` (Enterprise Tenant Root)
  2. `df_branches` (Operational Branch Locations)
  3. Scoped operational records (Orders, Stock, Employees, Invoices, Tables, etc.) carry Foreign Keys to `restaurant_id` and/or `branch_id`.
- **Composite Indexes**: Composite indexes on `(restaurant_id, branch_id, created_at)` enable sub-millisecond query isolation across high data volumes.

### 2.2 Base Model & Soft Deletion Pattern
Every operational table extends `BaseModel`, which provides:
- `id`: Globally unique UUIDv4 primary key (`UUIDField`) to eliminate sequential ID enumeration attacks.
- `created_at`: `DateTimeField` with `auto_now_add=True`, indexed for temporal queries.
- `updated_at`: `DateTimeField` with `auto_now=True`.
- `is_deleted`: `BooleanField(default=False, db_index=True)`.
- `deleted_at`: `DateTimeField(null=True, blank=True)`.

#### Soft Deletion Queryset & Managers
- `objects`: Default `SoftDeleteManager` filters out `is_deleted=True` automatically.
- `all_objects`: `AllObjectsManager` allows administrative and audit queries across active and deleted records.
- Soft delete operations execute via `.soft_delete()` and `.restore()`.

---

## 3. Domain Decomposition (24 Enterprise Subsystems)

The architecture is partitioned into 24 decoupled domain applications located under `apps/`:

| Subsystem Domain | Purpose & Scope | Key Models |
| :--- | :--- | :--- |
| **`core`** | Multi-tenancy roots, Users, Roles, Permissions | `User`, `Role`, `Permission`, `UserRole`, `Restaurant`, `Branch` |
| **`employees`** | HRMS, biometric attendance, shifts, leave, Indian payroll | `Employee`, `Department`, `Designation`, `Attendance`, `Shift`, `Payroll` |
| **`menu`** | Menu hierarchy, variants, addons, recipe Bill of Materials | `Menu`, `MenuCategory`, `MenuItem`, `MenuVariant`, `Recipe`, `FoodIngredient` |
| **`tables`** | Table sections, table occupancy states, reservations | `TableSection`, `RestaurantTable`, `Reservation`, `TableAssignment` |
| **`orders`** | Dine-in, Takeaway, Delivery lifecycle & tax/discount logs | `Order`, `OrderItem`, `OrderItemAddon`, `OrderStatusHistory`, `OrderTax` |
| **`kitchen`** | Kitchen Display System (KDS) & Kitchen Order Tickets | `KitchenStation`, `KitchenOrder`, `KitchenOrderItem`, `PreparationTimer` |
| **`inventory`** | Central stock ledger, batch tracking, waste, adjustments | `InventoryItem`, `Stock`, `StockBatch`, `StockMovement`, `WasteRecord` |
| **`suppliers`** | Vendor catalogs, procurement contracts, ratings | `Supplier`, `SupplierContact`, `SupplierProduct`, `SupplierPayment` |
| **`purchases`** | Purchase orders, Goods Received Notes (GRN) | `PurchaseOrder`, `PurchaseOrderItem`, `GoodsReceipt`, `GoodsReceiptItem` |
| **`billing`** | Tax invoice issuance, concurrency sequence locking | `Invoice`, `InvoiceItem`, `InvoiceTax`, `InvoiceNumberSequence` |
| **`payments`** | Cash, UPI, Card ledgers, refund workflows | `Payment`, `PaymentMethod`, `PaymentTransaction`, `Refund` |
| **`customers`** | CRM profiles, dietary preferences, order histories | `Customer`, `CustomerAddress`, `CustomerPreference`, `CustomerOrderHistory` |
| **`delivery`** | Rider dispatch, Swiggy/Zomato channel tracking | `DeliveryOrder`, `DeliveryAddress`, `DeliveryAssignment` |
| **`offers`** | Promotions, coupons, min order & max cap rules | `Offer`, `Coupon`, `CouponUsage`, `OfferMenuItem`, `OfferBranch` |
| **`loyalty`** | Tier multipliers, points transactions ledger, rewards | `CustomerTier`, `LoyaltyAccount`, `LoyaltyTransaction`, `Reward` |
| **`reviews`** | Customer ratings (1-5), owner responses, moderation | `Review`, `ReviewResponse`, `ReviewModeration` |
| **`expenses`** | Operational expenditure, categories, approvals | `ExpenseCategory`, `Expense`, `ExpenseApproval`, `ExpenseAttachment` |
| **`taxes`** | Indian GST engine (CGST 2.5% + SGST 2.5% / IGST 5%) | `TaxCategory`, `TaxRate`, `TaxRule`, `RestaurantTaxConfiguration` |
| **`notifications`** | Alert routing (in-app, SMS, email) | `Notification`, `NotificationPreference`, `NotificationReadStatus` |
| **`analytics`** | Daily/monthly sales snapshots, profitability, demand | `DailySalesSnapshot`, `MonthlySalesSnapshot`, `ProfitAnalytics` |
| **`ml`** | Forecasting models, features, training logs, predictions | `MLDataset`, `MLFeature`, `MLModel`, `MLModelVersion`, `MLPrediction` |
| **`reports`** | GSTR-1, GSTR-3B, P&L, Inventory valuation configs | `ReportDefinition`, `ReportExecution`, `ReportSchedule`, `ReportExport` |
| **`audit`** | Change Data Capture (CDC) audit trail & security events | `AuditLog`, `SecurityEvent`, `LoginHistory` |
| **`settings_app`**| System key-values and automated database backups | `SystemSetting`, `RestaurantSetting`, `BranchSetting`, `BackupRecord` |

---

## 4. Indian Statutory Tax (GST) Architecture

DineFlow includes an Indian GST calculation engine conforming to Central Board of Indirect Taxes and Customs (CBIC) standards:
- **Intra-State Transactions**:
  - `CGST`: 2.5%
  - `SGST`: 2.5%
  - Total Food Service GST = 5.0%
- **Inter-State Transactions**:
  - `IGST`: 5.0%
- **HSN / SAC Codes**:
  - `996331`: Restaurant service with air-conditioning or central heating.
  - `996332`: Takeaway / food pickup counter service.
- **Invoice Numbering**: Formatted as `{PREFIX}/{BRANCH_CODE}/{FISCAL_YEAR}/{SEQUENCE}` (e.g. `INV/HYD01/2026-27/00042`).
- **Pessimistic Locking**: `InvoiceNumberSequence` rows are locked via `select_for_update()` inside `transaction.atomic()` blocks to prevent concurrency gaps or duplicate numbers.

---

## 5. Automated Recipe Bill of Materials (BOM) Consumption

When an order is confirmed or marked as `PREPARING`, the `InventoryService` queries each line item's `Recipe` and attached `FoodIngredient`s. It calculates exact required quantities and atomically deducts them from `df_stocks`, while recording an immutable `StockMovement` of type `RECIPE_CONSUMPTION` with delta quantities and updated balances.

---

## 6. Database Engine Compatibility Strategy

1. **SQLite (Development / Testing)**:
   - Zero-configuration local development.
   - Fast ephemeral in-memory test execution.
   - Native online backup via SQLite file copying and connection iterdump.
2. **PostgreSQL (Production)**:
   - High concurrency with multi-version concurrency control (MVCC).
   - JSONB support for audit diffs and ML metadata.
   - Connection pooling with `CONN_MAX_AGE`.

# DineFlow Enterprise Data Dictionary

This document specifies the database table definitions, physical table identifiers (`df_*`), data types, nullability, default values, check constraints, and descriptions across the system.

---

## 1. Core Subsystem

### `df_restaurants` (Restaurant Entity)
| Column Name | Data Type | Nullable | Default | Constraints / Description |
| :--- | :--- | :--- | :--- | :--- |
| `id` | UUID | No | `uuid4` | Primary Key |
| `name` | VARCHAR(200) | No | - | Enterprise brand name |
| `legal_name` | VARCHAR(255) | No | - | Registered corporate business name |
| `code` | VARCHAR(50) | No | - | Unique enterprise code |
| `gstin` | VARCHAR(15) | Yes | '' | 15-character Indian GSTIN |
| `fssai_license`| VARCHAR(20) | Yes | '' | FSSAI Food Safety License Number |
| `pan_number` | VARCHAR(10) | Yes | '' | Corporate Income Tax PAN |
| `currency` | VARCHAR(10) | No | 'INR' | Default operational currency |
| `currency_symbol` | VARCHAR(5) | No | '₹' | Display symbol |
| `is_active` | BOOLEAN | No | True | Operational status |

### `df_branches` (Operational Branch)
| Column Name | Data Type | Nullable | Default | Constraints / Description |
| :--- | :--- | :--- | :--- | :--- |
| `id` | UUID | No | `uuid4` | Primary Key |
| `restaurant_id`| UUID | No | - | FK to `df_restaurants` (`CASCADE`) |
| `name` | VARCHAR(200) | No | - | Branch location title |
| `code` | VARCHAR(50) | No | - | Branch code (Unique per restaurant) |
| `city` | VARCHAR(100) | No | - | Operating city |
| `state` | VARCHAR(100) | No | - | Operating state (e.g. Telangana, Andhra Pradesh) |
| `pincode` | VARCHAR(10) | No | - | Postal PIN code |
| `latitude` | NUMERIC(9,6) | Yes | Null | Geolocation latitude |
| `longitude` | NUMERIC(9,6) | Yes | Null | Geolocation longitude |
| `is_active` | BOOLEAN | No | True | Active flag |

---

## 2. Order & Kitchen Subsystem

### `df_orders` (Order Header)
| Column Name | Data Type | Nullable | Default | Constraints / Description |
| :--- | :--- | :--- | :--- | :--- |
| `id` | UUID | No | `uuid4` | Primary Key |
| `branch_id` | UUID | No | - | FK to `df_branches` (`CASCADE`) |
| `order_number`| VARCHAR(50) | No | - | Unique system order identifier |
| `order_type` | VARCHAR(20) | No | 'DINE_IN' | Choices: `DINE_IN`, `TAKEAWAY`, `DELIVERY` |
| `status` | VARCHAR(20) | No | 'PLACED' | Choices: `PLACED`, `CONFIRMED`, `PREPARING`, `READY`, `SERVED`, `BILLED`, `PAID`, `COMPLETED`, `CANCELLED` |
| `subtotal` | NUMERIC(12,2)| No | 0.00 | Line items subtotal (`CHECK >= 0`) |
| `tax_amount` | NUMERIC(12,2)| No | 0.00 | Total GST computed (`CHECK >= 0`) |
| `discount_amount`| NUMERIC(12,2)| No| 0.00 | Concessions / coupons applied (`CHECK >= 0`) |
| `final_amount`| NUMERIC(12,2)| No | 0.00 | Payable total in INR (`CHECK >= 0`) |
| `placed_at` | TIMESTAMPTZ | No | `now` | Order placement timestamp |

### `df_order_items` (Order Line Items)
| Column Name | Data Type | Nullable | Default | Constraints / Description |
| :--- | :--- | :--- | :--- | :--- |
| `id` | UUID | No | `uuid4` | Primary Key |
| `order_id` | UUID | No | - | FK to `df_orders` (`CASCADE`) |
| `menu_item_id`| UUID | No | - | FK to `df_menu_items` (`PROTECT`) |
| `quantity` | INTEGER | No | 1 | Units ordered (`CHECK > 0`) |
| `unit_price` | NUMERIC(10,2)| No | - | Price per unit (`CHECK >= 0`) |
| `total_price` | NUMERIC(12,2)| No | - | Line total (`CHECK >= 0`) |
| `status` | VARCHAR(20) | No | 'RECEIVED' | Line status (`RECEIVED` to `SERVED`) |

---

## 3. Billing & Payments Subsystem

### `df_invoices` (Tax Invoices)
| Column Name | Data Type | Nullable | Default | Constraints / Description |
| :--- | :--- | :--- | :--- | :--- |
| `id` | UUID | No | `uuid4` | Primary Key |
| `order_id` | UUID | No | - | OneToOne to `df_orders` (`PROTECT`) |
| `branch_id` | UUID | No | - | FK to `df_branches` (`PROTECT`) |
| `invoice_number`| VARCHAR(60)| No| - | Unique invoice code (`INV/HYD01/2026-27/00001`) |
| `fiscal_year` | VARCHAR(10) | No | - | Fiscal Year (`2026-27`) |
| `subtotal` | NUMERIC(12,2)| No | - | Taxable value (`CHECK >= 0`) |
| `cgst_amount` | NUMERIC(12,2)| No | 0.00 | Central GST (2.5%) |
| `sgst_amount` | NUMERIC(12,2)| No | 0.00 | State GST (2.5%) |
| `igst_amount` | NUMERIC(12,2)| No | 0.00 | Integrated GST (5.0%) |
| `grand_total` | NUMERIC(12,2)| No | - | Final rounded total in INR |
| `qr_code_data`| TEXT | Yes | '' | B2C UPI payment URI payload |

### `df_payments` (Settlement Ledger)
| Column Name | Data Type | Nullable | Default | Constraints / Description |
| :--- | :--- | :--- | :--- | :--- |
| `id` | UUID | No | `uuid4` | Primary Key |
| `invoice_id` | UUID | No | - | FK to `df_invoices` (`PROTECT`) |
| `payment_method_id`| UUID | No| - | FK to `df_payment_methods` (`PROTECT`) |
| `amount` | NUMERIC(12,2)| No | - | Paid amount (`CHECK > 0`) |
| `transaction_reference`| VARCHAR(100)| Yes| '' | Bank UTR / Card Auth / Cash Slip |
| `status` | VARCHAR(20) | No | 'SUCCESS' | Choices: `INITIATED`, `SUCCESS`, `FAILED`, `REFUNDED` |

---

## 4. Inventory & Procurement Subsystem

### `df_stocks` (Branch Inventory Balance)
| Column Name | Data Type | Nullable | Default | Constraints / Description |
| :--- | :--- | :--- | :--- | :--- |
| `id` | UUID | No | `uuid4` | Primary Key |
| `branch_id` | UUID | No | - | FK to `df_branches` |
| `inventory_item_id`| UUID | No| - | FK to `df_inventory_items` |
| `quantity_on_hand`| NUMERIC(12,3)| No| 0.000 | Physical balance on site (`CHECK >= 0`) |
| `available_quantity`| NUMERIC(12,3)| No| 0.000 | Unreserved available stock (`CHECK >= 0`) |
| `reserved_quantity` | NUMERIC(12,3)| No| 0.000 | Stock allocated to active prep |

### `df_stock_movements` (Immutable Movement Ledger)
| Column Name | Data Type | Nullable | Default | Constraints / Description |
| :--- | :--- | :--- | :--- | :--- |
| `id` | UUID | No | `uuid4` | Primary Key |
| `branch_id` | UUID | No | - | FK to `df_branches` |
| `inventory_item_id`| UUID | No| - | FK to `df_inventory_items` |
| `movement_type`| VARCHAR(30)| No | - | `PURCHASE_RECEIPT`, `RECIPE_CONSUMPTION`, `WASTAGE`, `ADJUSTMENT_ADD`, `ADJUSTMENT_SUB` |
| `quantity` | NUMERIC(12,3)| No | - | Delta (+ / -) |
| `balance_before`| NUMERIC(12,3)| No| - | Balance preceding operation |
| `balance_after` | NUMERIC(12,3)| No| - | Resulting balance |
| `reference_id` | VARCHAR(100)| Yes| '' | PO, GRN, or Order identifier |

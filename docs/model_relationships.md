# DineFlow Model Relationships and Referential Integrity Guide

This document details the foreign key relationships, cardinalities, cascade behaviors, and integrity safeguards across the DineFlow database.

## 1. Referential Deletion Rules

| Relationship Type | On-Delete Strategy | Justification |
| :--- | :--- | :--- |
| **Financial / Tax Records** | `models.PROTECT` | Invoices, Payments, Tax Configurations, and Payroll records cannot be deleted if referenced, guaranteeing auditability and GST compliance. |
| **Inventory & Procurement** | `models.PROTECT` | Suppliers and Inventory Items tied to historic Stock Movements or Purchase Orders are protected against accidental deletion. |
| **Organizational Ownership** | `models.CASCADE` | Deleting a test tenant or branch removes its owned tables, sections, and private settings. |
| **Operational Actors** | `models.SET_NULL` | If a waiter, cashier, or approver user profile is terminated, transaction records retain history while setting the actor foreign key to null. |

---

## 2. Cardinality and Mapping Matrix

### Core & Multi-Tenancy
- **`Restaurant` 1:N `Branch`**: One restaurant enterprise owns multiple branches (`on_delete=CASCADE`).
- **`Restaurant` 1:1 `RestaurantSettings`**: Unique configuration per restaurant tenant (`on_delete=CASCADE`).
- **`Branch` 1:1 `BranchSettings`**: Operational settings per location (`on_delete=CASCADE`).
- **`User` M:N `Role` via `UserRole`**: Multi-tenant authorization scoped by restaurant or branch.

### Menu & Recipe BOM
- **`Menu` 1:N `MenuCategory`**: Categories within a menu catalog (`on_delete=CASCADE`).
- **`MenuCategory` 1:N `MenuItem`**: Dishes grouped under a category (`on_delete=CASCADE`).
- **`MenuItem` 1:N `MenuVariant`**: Portion sizes/variations for a dish (`on_delete=CASCADE`).
- **`MenuItem` 1:1 `Recipe`**: Standard Operating Procedure recipe for an item (`on_delete=CASCADE`).
- **`Recipe` 1:N `FoodIngredient`**: Ingredients (BOM) needed per serving (`on_delete=CASCADE`).
- **`InventoryItem` 1:N `FoodIngredient`**: Referenced with `models.PROTECT`.

### Orders & Kitchen
- **`Branch` 1:N `Order`**: Orders received at a branch location (`on_delete=CASCADE`).
- **`Customer` 1:N `Order`**: Customer placing the order (`on_delete=SET_NULL`).
- **`RestaurantTable` 1:N `Order`**: Active or historic dine-in table (`on_delete=SET_NULL`).
- **`Order` 1:N `OrderItem`**: Line items inside an order (`on_delete=CASCADE`).
- **`MenuItem` 1:N `OrderItem`**: Item ordered (`on_delete=PROTECT`).
- **`Order` 1:N `KitchenOrder`**: KOT tickets dispatched to kitchen stations (`on_delete=CASCADE`).
- **`KitchenStation` 1:N `KitchenOrder`**: Target station (`on_delete=SET_NULL`).

### Billing & Payments
- **`Order` 1:1 `Invoice`**: One fiscal tax invoice generated per completed bill (`on_delete=PROTECT`).
- **`Invoice` 1:N `InvoiceItem`**: Itemized lines on the tax invoice (`on_delete=CASCADE`).
- **`Invoice` 1:N `InvoiceTax`**: Breakdown of CGST, SGST, IGST (`on_delete=CASCADE`).
- **`Invoice` 1:N `Payment`**: Tenders collected for an invoice (`on_delete=PROTECT`).
- **`Payment` 1:N `PaymentTransaction`**: Audit ledger of transaction attempts (`on_delete=CASCADE`).
- **`Payment` 1:N `Refund`**: Reversals against payments (`on_delete=PROTECT`).

### Inventory Ledger
- **`Branch` 1:N `Stock`**: Current on-hand quantity per item at a branch (`on_delete=CASCADE`).
- **`InventoryItem` 1:N `Stock`**: Item inventory status (`on_delete=CASCADE`).
- **`Stock` 1:N `StockMovement`**: Complete immutable ledger for every stock delta (`on_delete=CASCADE`).
- **`StockBatch` 1:N `StockMovement`**: Specific batch tracking (`on_delete=SET_NULL`).

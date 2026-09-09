# DineFlow ERP — Role-Based Access Control (RBAC) Permissions Matrix

DineFlow implements a strict 10-role enterprise security and access architecture. Every HTTP request and domain service is guarded by role verification decorators (`@role_required`, `@module_permission_required`).

---

## 1. Enterprise Roles Defined

| Role Code | Role Name | Primary Responsibility | Default Workspace |
| :--- | :--- | :--- | :--- |
| `SUPER_ADMIN` | Super Administrator | Global system governance, database maintenance, multi-tenant setup | Entire System |
| `RESTAURANT_OWNER`| Restaurant Owner | Executive financial oversight, profit margins, branch expansion | Executive Dashboard |
| `MANAGER` | General Branch Manager | Day-to-day operations, discounts, staff rosters, expense approvals | Branch Operations |
| `KITCHEN_STAFF` | Kitchen Staff / Chef | Kitchen Display System (KDS), ticket bump actions, recipe view | KDS Live Screen |
| `WAITER` | Steward / Waiter | Table layout, order creation, item modifications, guest service | POS Dine-in Floor |
| `CASHIER` | Cashier / Billing Agent| Bill generation, invoice split, cash drawer reconciliation, payments | Billing & Cash Register |
| `INVENTORY_MANAGER`| Inventory & Stock Manager| Raw ingredient tracking, POs, inward receipts, supplier relations| Inventory & Procurement |
| `HR` | Human Resources Manager | Staff onboarding, KYC compliance, punch clock, Indian payroll | HR & Payroll Suite |
| `ANALYTICS_USER` | Business Analyst | Sales analytics, ML demand forecasts, turnover reports | Analytics Hub |
| `CUSTOMER` | Guest / Customer | Profile preferences, loyalty points balance, dining history | Customer Portal |

---

## 2. Granular Module Permissions Matrix

Legend:
- `FULL`: Complete administrative CRUD privileges (Create, Read, Update, Delete, Approve).
- `OPERATE`: Operational execution (Create, Read, Update assigned records).
- `READ`: Read-only reporting and lookup access.
- `--`: Access Denied (Raises HTTP 403 `PermissionDenied`).

| Domain App / Capability | SUPER_ADMIN | RESTAURANT_OWNER | MANAGER | KITCHEN_STAFF | WAITER | CASHIER | INVENTORY_MANAGER | HR | ANALYTICS_USER | CUSTOMER |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **System Settings & Config** | `FULL` | `READ` | `READ` | `--` | `--` | `--` | `--` | `--` | `--` | `--` |
| **Branch Management** | `FULL` | `FULL` | `READ` | `--` | `--` | `--` | `--` | `--` | `--` | `--` |
| **User & Staff Governance** | `FULL` | `FULL` | `OPERATE` | `--` | `--` | `--` | `--` | `FULL` | `--` | `--` |
| **Floor Plan & Tables** | `FULL` | `READ` | `FULL` | `READ` | `OPERATE` | `READ` | `--` | `--` | `READ` | `--` |
| **Menu Catalog & Pricing** | `FULL` | `FULL` | `OPERATE` | `READ` | `READ` | `READ` | `--` | `--` | `READ` | `READ` |
| **POS Order Placement** | `FULL` | `READ` | `FULL` | `--` | `FULL` | `OPERATE` | `--` | `--` | `--` | `--` |
| **Kitchen KDS & Bump Bar** | `FULL` | `READ` | `FULL` | `FULL` | `READ` | `--` | `--` | `--` | `--` | `--` |
| **Tax Invoicing & Billing** | `FULL` | `READ` | `FULL` | `--` | `--` | `FULL` | `--` | `--` | `READ` | `--` |
| **Payment Collection** | `FULL` | `READ` | `FULL` | `--` | `--` | `FULL` | `--` | `--` | `--` | `--` |
| **Cash Drawer & Z-Reports** | `FULL` | `FULL` | `FULL` | `--` | `--` | `OPERATE` | `--` | `--` | `READ` | `--` |
| **Raw Material Inventory** | `FULL` | `READ` | `FULL` | `READ` | `--` | `--` | `FULL` | `--` | `READ` | `--` |
| **BOM Recipe Management** | `FULL` | `READ` | `FULL` | `READ` | `--` | `--` | `OPERATE` | `--` | `--` | `--` |
| **Suppliers & Purchases** | `FULL` | `READ` | `FULL` | `--` | `--` | `--` | `FULL` | `--` | `READ` | `--` |
| **HR & KYC Profiles** | `FULL` | `READ` | `OPERATE` | `--` | `--` | `--` | `--` | `FULL` | `--` | `--` |
| **Shifts & Attendance** | `FULL` | `READ` | `FULL` | `OPERATE` | `OPERATE`| `OPERATE`| `OPERATE` | `FULL` | `READ` | `--` |
| **Indian Statutory Payroll** | `FULL` | `FULL` | `READ` | `--` | `--` | `--` | `--` | `FULL` | `--` | `--` |
| **Operating Expenses** | `FULL` | `FULL` | `FULL` | `OPERATE` | `--` | `OPERATE`| `OPERATE` | `--` | `READ` | `--` |
| **Customer CRM & Loyalty** | `FULL` | `READ` | `FULL` | `--` | `READ` | `OPERATE` | `--` | `--` | `READ` | `OPERATE`|
| **Machine Learning Demand** | `FULL` | `FULL` | `FULL` | `--` | `--` | `--` | `READ` | `--` | `FULL` | `--` |
| **Audit Logs & Traceability**| `FULL` | `FULL` | `READ` | `--` | `--` | `--` | `--` | `--` | `--` | `--` |

---

## 3. Enforcement Implementation

### View-Level Decorator: `@role_required`
```python
from apps.accounts.decorators import role_required
from apps.accounts.models import RoleChoices

@role_required(RoleChoices.MANAGER, RoleChoices.SUPER_ADMIN)
def approve_expense_view(request, expense_id):
    # Only Managers and Super Admins can execute approval
    ...
```

### Module-Level Decorator: `@module_permission_required`
```python
from apps.accounts.decorators import module_permission_required

@module_permission_required('payroll')
def generate_monthly_payslips(request):
    # Verifies user role has permission to access the HR/Payroll domain
    ...
```

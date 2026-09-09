# DineFlow ERP — Security Architecture & Hardening Standards

This document establishes the enterprise security guidelines, access policies, and cryptographic controls implemented across DineFlow.

---

## 1. Authentication & Credential Hardening

1. **Password Hashing**:
   - Uses Django's PBKDF2 algorithm with SHA-256 hash and salt (or Argon2 in production). Plaintext passwords are never stored in memory or persistence.
2. **Brute-Force & Lockout Defense**:
   - `failed_login_attempts` tracks invalid login attempts on user accounts.
   - Upon reaching 5 consecutive failures, `is_locked` is set to `True` with `locked_until = now() + 15 minutes`.
   - Successful authentication resets the counter to 0.
3. **Session Management**:
   - Session cookies utilize `HTTPOnly = True` preventing client-side JavaScript access and XSS token theft.
   - Default session duration: 12 hours for back-office personnel, with auto-timeout on POS terminals.

---

## 2. Multi-Tenant Branch Isolation

1. **Tenancy Boundaries**:
   - Every operational transaction (`Order`, `Invoice`, `StockMovement`, `Expense`, `CashRegisterSession`) is bound to a specific `Branch`.
2. **Query Isolation**:
   - Branch Managers and operational staff are restricted to querying and updating data belonging exclusively to their assigned branch.
   - Cross-branch aggregate visibility is restricted to `SUPER_ADMIN`, `RESTAURANT_OWNER`, and `ANALYTICS_USER` roles.

---

## 3. Defense Against OWASP Top 10 Vulnerabilities

| Vulnerability | DineFlow Defense Architecture |
| :--- | :--- |
| **SQL Injection (SQLi)** | 100% of database interactions execute through Django ORM's parameterized query engine. Raw string SQL formatting is strictly forbidden. |
| **Cross-Site Scripting (XSS)**| Django template auto-escaping is active across all 68 templates. Untrusted customer inputs (guest reviews, special cooking notes) are escaped. |
| **Cross-Site Request Forgery (CSRF)** | Standard Django CSRF middleware enforces cryptographically signed CSRF tokens on all modifying HTTP POST, PUT, and DELETE forms. |
| **Broken Object Level Auth (BOLA)** | Every detail view and API endpoint validates that the target object belongs to the authenticated user's assigned branch and permitted role. |
| **Security Misconfiguration** | Debug mode is disabled in production environments (`DEBUG = False`), with strict `ALLOWED_HOSTS` enforcement. |

---

## 4. Immutable Audit Trail & Change Logging

Critical business operations are recorded in the `audit_auditlog` table:
- **Captured Events**:
  - `PRICE_CHANGE`: Menu dish base price modifications.
  - `ORDER_CANCEL`: Cancellation of active orders with mandatory reason.
  - `REFUND_APPROVE`: Financial payouts or bill adjustments.
  - `STOCK_ADJUST`: Discrepancies identified during physical warehouse stock counts.
  - `PAYROLL_RUN`: Monthly salary disbursals and approvals.
- **Audit Attributes**: Actor ID, Action Enum, Target Model, Target Object ID, Client IP Address, Timestamp, and JSON state diff (`old_values` vs `new_values`).
- **Immutability**: Audit log records cannot be updated or deleted via application UI.

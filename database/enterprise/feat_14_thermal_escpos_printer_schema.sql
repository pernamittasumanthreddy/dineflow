-- DineFlow Enterprise Schema Extension
-- Feature: Thermal 80mm ESC/POS Receipt Formatter and Print Spooler (thermal-escpos-printer)
-- Optimized for PostgreSQL and SQLite Compatibility

CREATE TABLE IF NOT EXISTS df_billing_thermal_escpos_printer_01 (
    id VARCHAR(36) PRIMARY KEY,
    restaurant_id VARCHAR(36) NOT NULL,
    branch_id VARCHAR(36) NOT NULL,
    code VARCHAR(50) NOT NULL,
    title VARCHAR(200) NOT NULL,
    taxable_amount DECIMAL(12, 2) DEFAULT 0.00,
    cgst_rate DECIMAL(5, 2) DEFAULT 2.50,
    sgst_rate DECIMAL(5, 2) DEFAULT 2.50,
    igst_rate DECIMAL(5, 2) DEFAULT 5.00,
    total_amount DECIMAL(12, 2) DEFAULT 0.00,
    currency VARCHAR(5) DEFAULT "INR",
    is_active BOOLEAN DEFAULT TRUE,
    metadata TEXT DEFAULT "{}",
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_df_billing_thermal_escpos_printer_01_rest_branch 
ON df_billing_thermal_escpos_printer_01(restaurant_id, branch_id);

CREATE TABLE IF NOT EXISTS df_billing_thermal_escpos_printer_02 (
    id VARCHAR(36) PRIMARY KEY,
    restaurant_id VARCHAR(36) NOT NULL,
    branch_id VARCHAR(36) NOT NULL,
    code VARCHAR(50) NOT NULL,
    title VARCHAR(200) NOT NULL,
    taxable_amount DECIMAL(12, 2) DEFAULT 0.00,
    cgst_rate DECIMAL(5, 2) DEFAULT 2.50,
    sgst_rate DECIMAL(5, 2) DEFAULT 2.50,
    igst_rate DECIMAL(5, 2) DEFAULT 5.00,
    total_amount DECIMAL(12, 2) DEFAULT 0.00,
    currency VARCHAR(5) DEFAULT "INR",
    is_active BOOLEAN DEFAULT TRUE,
    metadata TEXT DEFAULT "{}",
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_df_billing_thermal_escpos_printer_02_rest_branch 
ON df_billing_thermal_escpos_printer_02(restaurant_id, branch_id);

CREATE TABLE IF NOT EXISTS df_billing_thermal_escpos_printer_03 (
    id VARCHAR(36) PRIMARY KEY,
    restaurant_id VARCHAR(36) NOT NULL,
    branch_id VARCHAR(36) NOT NULL,
    code VARCHAR(50) NOT NULL,
    title VARCHAR(200) NOT NULL,
    taxable_amount DECIMAL(12, 2) DEFAULT 0.00,
    cgst_rate DECIMAL(5, 2) DEFAULT 2.50,
    sgst_rate DECIMAL(5, 2) DEFAULT 2.50,
    igst_rate DECIMAL(5, 2) DEFAULT 5.00,
    total_amount DECIMAL(12, 2) DEFAULT 0.00,
    currency VARCHAR(5) DEFAULT "INR",
    is_active BOOLEAN DEFAULT TRUE,
    metadata TEXT DEFAULT "{}",
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_df_billing_thermal_escpos_printer_03_rest_branch 
ON df_billing_thermal_escpos_printer_03(restaurant_id, branch_id);

CREATE TABLE IF NOT EXISTS df_billing_thermal_escpos_printer_04 (
    id VARCHAR(36) PRIMARY KEY,
    restaurant_id VARCHAR(36) NOT NULL,
    branch_id VARCHAR(36) NOT NULL,
    code VARCHAR(50) NOT NULL,
    title VARCHAR(200) NOT NULL,
    taxable_amount DECIMAL(12, 2) DEFAULT 0.00,
    cgst_rate DECIMAL(5, 2) DEFAULT 2.50,
    sgst_rate DECIMAL(5, 2) DEFAULT 2.50,
    igst_rate DECIMAL(5, 2) DEFAULT 5.00,
    total_amount DECIMAL(12, 2) DEFAULT 0.00,
    currency VARCHAR(5) DEFAULT "INR",
    is_active BOOLEAN DEFAULT TRUE,
    metadata TEXT DEFAULT "{}",
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_df_billing_thermal_escpos_printer_04_rest_branch 
ON df_billing_thermal_escpos_printer_04(restaurant_id, branch_id);

CREATE TABLE IF NOT EXISTS df_billing_thermal_escpos_printer_05 (
    id VARCHAR(36) PRIMARY KEY,
    restaurant_id VARCHAR(36) NOT NULL,
    branch_id VARCHAR(36) NOT NULL,
    code VARCHAR(50) NOT NULL,
    title VARCHAR(200) NOT NULL,
    taxable_amount DECIMAL(12, 2) DEFAULT 0.00,
    cgst_rate DECIMAL(5, 2) DEFAULT 2.50,
    sgst_rate DECIMAL(5, 2) DEFAULT 2.50,
    igst_rate DECIMAL(5, 2) DEFAULT 5.00,
    total_amount DECIMAL(12, 2) DEFAULT 0.00,
    currency VARCHAR(5) DEFAULT "INR",
    is_active BOOLEAN DEFAULT TRUE,
    metadata TEXT DEFAULT "{}",
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_df_billing_thermal_escpos_printer_05_rest_branch 
ON df_billing_thermal_escpos_printer_05(restaurant_id, branch_id);

CREATE TABLE IF NOT EXISTS df_billing_thermal_escpos_printer_06 (
    id VARCHAR(36) PRIMARY KEY,
    restaurant_id VARCHAR(36) NOT NULL,
    branch_id VARCHAR(36) NOT NULL,
    code VARCHAR(50) NOT NULL,
    title VARCHAR(200) NOT NULL,
    taxable_amount DECIMAL(12, 2) DEFAULT 0.00,
    cgst_rate DECIMAL(5, 2) DEFAULT 2.50,
    sgst_rate DECIMAL(5, 2) DEFAULT 2.50,
    igst_rate DECIMAL(5, 2) DEFAULT 5.00,
    total_amount DECIMAL(12, 2) DEFAULT 0.00,
    currency VARCHAR(5) DEFAULT "INR",
    is_active BOOLEAN DEFAULT TRUE,
    metadata TEXT DEFAULT "{}",
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_df_billing_thermal_escpos_printer_06_rest_branch 
ON df_billing_thermal_escpos_printer_06(restaurant_id, branch_id);

CREATE TABLE IF NOT EXISTS df_billing_thermal_escpos_printer_07 (
    id VARCHAR(36) PRIMARY KEY,
    restaurant_id VARCHAR(36) NOT NULL,
    branch_id VARCHAR(36) NOT NULL,
    code VARCHAR(50) NOT NULL,
    title VARCHAR(200) NOT NULL,
    taxable_amount DECIMAL(12, 2) DEFAULT 0.00,
    cgst_rate DECIMAL(5, 2) DEFAULT 2.50,
    sgst_rate DECIMAL(5, 2) DEFAULT 2.50,
    igst_rate DECIMAL(5, 2) DEFAULT 5.00,
    total_amount DECIMAL(12, 2) DEFAULT 0.00,
    currency VARCHAR(5) DEFAULT "INR",
    is_active BOOLEAN DEFAULT TRUE,
    metadata TEXT DEFAULT "{}",
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_df_billing_thermal_escpos_printer_07_rest_branch 
ON df_billing_thermal_escpos_printer_07(restaurant_id, branch_id);

CREATE TABLE IF NOT EXISTS df_billing_thermal_escpos_printer_08 (
    id VARCHAR(36) PRIMARY KEY,
    restaurant_id VARCHAR(36) NOT NULL,
    branch_id VARCHAR(36) NOT NULL,
    code VARCHAR(50) NOT NULL,
    title VARCHAR(200) NOT NULL,
    taxable_amount DECIMAL(12, 2) DEFAULT 0.00,
    cgst_rate DECIMAL(5, 2) DEFAULT 2.50,
    sgst_rate DECIMAL(5, 2) DEFAULT 2.50,
    igst_rate DECIMAL(5, 2) DEFAULT 5.00,
    total_amount DECIMAL(12, 2) DEFAULT 0.00,
    currency VARCHAR(5) DEFAULT "INR",
    is_active BOOLEAN DEFAULT TRUE,
    metadata TEXT DEFAULT "{}",
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_df_billing_thermal_escpos_printer_08_rest_branch 
ON df_billing_thermal_escpos_printer_08(restaurant_id, branch_id);

CREATE TABLE IF NOT EXISTS df_billing_thermal_escpos_printer_09 (
    id VARCHAR(36) PRIMARY KEY,
    restaurant_id VARCHAR(36) NOT NULL,
    branch_id VARCHAR(36) NOT NULL,
    code VARCHAR(50) NOT NULL,
    title VARCHAR(200) NOT NULL,
    taxable_amount DECIMAL(12, 2) DEFAULT 0.00,
    cgst_rate DECIMAL(5, 2) DEFAULT 2.50,
    sgst_rate DECIMAL(5, 2) DEFAULT 2.50,
    igst_rate DECIMAL(5, 2) DEFAULT 5.00,
    total_amount DECIMAL(12, 2) DEFAULT 0.00,
    currency VARCHAR(5) DEFAULT "INR",
    is_active BOOLEAN DEFAULT TRUE,
    metadata TEXT DEFAULT "{}",
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_df_billing_thermal_escpos_printer_09_rest_branch 
ON df_billing_thermal_escpos_printer_09(restaurant_id, branch_id);

CREATE TABLE IF NOT EXISTS df_billing_thermal_escpos_printer_10 (
    id VARCHAR(36) PRIMARY KEY,
    restaurant_id VARCHAR(36) NOT NULL,
    branch_id VARCHAR(36) NOT NULL,
    code VARCHAR(50) NOT NULL,
    title VARCHAR(200) NOT NULL,
    taxable_amount DECIMAL(12, 2) DEFAULT 0.00,
    cgst_rate DECIMAL(5, 2) DEFAULT 2.50,
    sgst_rate DECIMAL(5, 2) DEFAULT 2.50,
    igst_rate DECIMAL(5, 2) DEFAULT 5.00,
    total_amount DECIMAL(12, 2) DEFAULT 0.00,
    currency VARCHAR(5) DEFAULT "INR",
    is_active BOOLEAN DEFAULT TRUE,
    metadata TEXT DEFAULT "{}",
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_df_billing_thermal_escpos_printer_10_rest_branch 
ON df_billing_thermal_escpos_printer_10(restaurant_id, branch_id);

CREATE TABLE IF NOT EXISTS df_billing_thermal_escpos_printer_11 (
    id VARCHAR(36) PRIMARY KEY,
    restaurant_id VARCHAR(36) NOT NULL,
    branch_id VARCHAR(36) NOT NULL,
    code VARCHAR(50) NOT NULL,
    title VARCHAR(200) NOT NULL,
    taxable_amount DECIMAL(12, 2) DEFAULT 0.00,
    cgst_rate DECIMAL(5, 2) DEFAULT 2.50,
    sgst_rate DECIMAL(5, 2) DEFAULT 2.50,
    igst_rate DECIMAL(5, 2) DEFAULT 5.00,
    total_amount DECIMAL(12, 2) DEFAULT 0.00,
    currency VARCHAR(5) DEFAULT "INR",
    is_active BOOLEAN DEFAULT TRUE,
    metadata TEXT DEFAULT "{}",
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_df_billing_thermal_escpos_printer_11_rest_branch 
ON df_billing_thermal_escpos_printer_11(restaurant_id, branch_id);

CREATE TABLE IF NOT EXISTS df_billing_thermal_escpos_printer_12 (
    id VARCHAR(36) PRIMARY KEY,
    restaurant_id VARCHAR(36) NOT NULL,
    branch_id VARCHAR(36) NOT NULL,
    code VARCHAR(50) NOT NULL,
    title VARCHAR(200) NOT NULL,
    taxable_amount DECIMAL(12, 2) DEFAULT 0.00,
    cgst_rate DECIMAL(5, 2) DEFAULT 2.50,
    sgst_rate DECIMAL(5, 2) DEFAULT 2.50,
    igst_rate DECIMAL(5, 2) DEFAULT 5.00,
    total_amount DECIMAL(12, 2) DEFAULT 0.00,
    currency VARCHAR(5) DEFAULT "INR",
    is_active BOOLEAN DEFAULT TRUE,
    metadata TEXT DEFAULT "{}",
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_df_billing_thermal_escpos_printer_12_rest_branch 
ON df_billing_thermal_escpos_printer_12(restaurant_id, branch_id);

CREATE TABLE IF NOT EXISTS df_billing_thermal_escpos_printer_13 (
    id VARCHAR(36) PRIMARY KEY,
    restaurant_id VARCHAR(36) NOT NULL,
    branch_id VARCHAR(36) NOT NULL,
    code VARCHAR(50) NOT NULL,
    title VARCHAR(200) NOT NULL,
    taxable_amount DECIMAL(12, 2) DEFAULT 0.00,
    cgst_rate DECIMAL(5, 2) DEFAULT 2.50,
    sgst_rate DECIMAL(5, 2) DEFAULT 2.50,
    igst_rate DECIMAL(5, 2) DEFAULT 5.00,
    total_amount DECIMAL(12, 2) DEFAULT 0.00,
    currency VARCHAR(5) DEFAULT "INR",
    is_active BOOLEAN DEFAULT TRUE,
    metadata TEXT DEFAULT "{}",
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_df_billing_thermal_escpos_printer_13_rest_branch 
ON df_billing_thermal_escpos_printer_13(restaurant_id, branch_id);

CREATE TABLE IF NOT EXISTS df_billing_thermal_escpos_printer_14 (
    id VARCHAR(36) PRIMARY KEY,
    restaurant_id VARCHAR(36) NOT NULL,
    branch_id VARCHAR(36) NOT NULL,
    code VARCHAR(50) NOT NULL,
    title VARCHAR(200) NOT NULL,
    taxable_amount DECIMAL(12, 2) DEFAULT 0.00,
    cgst_rate DECIMAL(5, 2) DEFAULT 2.50,
    sgst_rate DECIMAL(5, 2) DEFAULT 2.50,
    igst_rate DECIMAL(5, 2) DEFAULT 5.00,
    total_amount DECIMAL(12, 2) DEFAULT 0.00,
    currency VARCHAR(5) DEFAULT "INR",
    is_active BOOLEAN DEFAULT TRUE,
    metadata TEXT DEFAULT "{}",
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_df_billing_thermal_escpos_printer_14_rest_branch 
ON df_billing_thermal_escpos_printer_14(restaurant_id, branch_id);

CREATE TABLE IF NOT EXISTS df_billing_thermal_escpos_printer_15 (
    id VARCHAR(36) PRIMARY KEY,
    restaurant_id VARCHAR(36) NOT NULL,
    branch_id VARCHAR(36) NOT NULL,
    code VARCHAR(50) NOT NULL,
    title VARCHAR(200) NOT NULL,
    taxable_amount DECIMAL(12, 2) DEFAULT 0.00,
    cgst_rate DECIMAL(5, 2) DEFAULT 2.50,
    sgst_rate DECIMAL(5, 2) DEFAULT 2.50,
    igst_rate DECIMAL(5, 2) DEFAULT 5.00,
    total_amount DECIMAL(12, 2) DEFAULT 0.00,
    currency VARCHAR(5) DEFAULT "INR",
    is_active BOOLEAN DEFAULT TRUE,
    metadata TEXT DEFAULT "{}",
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_df_billing_thermal_escpos_printer_15_rest_branch 
ON df_billing_thermal_escpos_printer_15(restaurant_id, branch_id);

CREATE TABLE IF NOT EXISTS df_billing_thermal_escpos_printer_16 (
    id VARCHAR(36) PRIMARY KEY,
    restaurant_id VARCHAR(36) NOT NULL,
    branch_id VARCHAR(36) NOT NULL,
    code VARCHAR(50) NOT NULL,
    title VARCHAR(200) NOT NULL,
    taxable_amount DECIMAL(12, 2) DEFAULT 0.00,
    cgst_rate DECIMAL(5, 2) DEFAULT 2.50,
    sgst_rate DECIMAL(5, 2) DEFAULT 2.50,
    igst_rate DECIMAL(5, 2) DEFAULT 5.00,
    total_amount DECIMAL(12, 2) DEFAULT 0.00,
    currency VARCHAR(5) DEFAULT "INR",
    is_active BOOLEAN DEFAULT TRUE,
    metadata TEXT DEFAULT "{}",
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_df_billing_thermal_escpos_printer_16_rest_branch 
ON df_billing_thermal_escpos_printer_16(restaurant_id, branch_id);

CREATE TABLE IF NOT EXISTS df_billing_thermal_escpos_printer_17 (
    id VARCHAR(36) PRIMARY KEY,
    restaurant_id VARCHAR(36) NOT NULL,
    branch_id VARCHAR(36) NOT NULL,
    code VARCHAR(50) NOT NULL,
    title VARCHAR(200) NOT NULL,
    taxable_amount DECIMAL(12, 2) DEFAULT 0.00,
    cgst_rate DECIMAL(5, 2) DEFAULT 2.50,
    sgst_rate DECIMAL(5, 2) DEFAULT 2.50,
    igst_rate DECIMAL(5, 2) DEFAULT 5.00,
    total_amount DECIMAL(12, 2) DEFAULT 0.00,
    currency VARCHAR(5) DEFAULT "INR",
    is_active BOOLEAN DEFAULT TRUE,
    metadata TEXT DEFAULT "{}",
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_df_billing_thermal_escpos_printer_17_rest_branch 
ON df_billing_thermal_escpos_printer_17(restaurant_id, branch_id);

CREATE TABLE IF NOT EXISTS df_billing_thermal_escpos_printer_18 (
    id VARCHAR(36) PRIMARY KEY,
    restaurant_id VARCHAR(36) NOT NULL,
    branch_id VARCHAR(36) NOT NULL,
    code VARCHAR(50) NOT NULL,
    title VARCHAR(200) NOT NULL,
    taxable_amount DECIMAL(12, 2) DEFAULT 0.00,
    cgst_rate DECIMAL(5, 2) DEFAULT 2.50,
    sgst_rate DECIMAL(5, 2) DEFAULT 2.50,
    igst_rate DECIMAL(5, 2) DEFAULT 5.00,
    total_amount DECIMAL(12, 2) DEFAULT 0.00,
    currency VARCHAR(5) DEFAULT "INR",
    is_active BOOLEAN DEFAULT TRUE,
    metadata TEXT DEFAULT "{}",
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_df_billing_thermal_escpos_printer_18_rest_branch 
ON df_billing_thermal_escpos_printer_18(restaurant_id, branch_id);

CREATE TABLE IF NOT EXISTS df_billing_thermal_escpos_printer_19 (
    id VARCHAR(36) PRIMARY KEY,
    restaurant_id VARCHAR(36) NOT NULL,
    branch_id VARCHAR(36) NOT NULL,
    code VARCHAR(50) NOT NULL,
    title VARCHAR(200) NOT NULL,
    taxable_amount DECIMAL(12, 2) DEFAULT 0.00,
    cgst_rate DECIMAL(5, 2) DEFAULT 2.50,
    sgst_rate DECIMAL(5, 2) DEFAULT 2.50,
    igst_rate DECIMAL(5, 2) DEFAULT 5.00,
    total_amount DECIMAL(12, 2) DEFAULT 0.00,
    currency VARCHAR(5) DEFAULT "INR",
    is_active BOOLEAN DEFAULT TRUE,
    metadata TEXT DEFAULT "{}",
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_df_billing_thermal_escpos_printer_19_rest_branch 
ON df_billing_thermal_escpos_printer_19(restaurant_id, branch_id);

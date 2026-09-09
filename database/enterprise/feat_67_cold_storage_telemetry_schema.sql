-- DineFlow Enterprise Schema Extension
-- Feature: IoT Cold Storage Temperature Sensors and Power Failure Alarms (cold-storage-telemetry)
-- Optimized for PostgreSQL and SQLite Compatibility

CREATE TABLE IF NOT EXISTS df_inventory_cold_storage_telemetry_01 (
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

CREATE INDEX IF NOT EXISTS idx_df_inventory_cold_storage_telemetry_01_rest_branch 
ON df_inventory_cold_storage_telemetry_01(restaurant_id, branch_id);

CREATE TABLE IF NOT EXISTS df_inventory_cold_storage_telemetry_02 (
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

CREATE INDEX IF NOT EXISTS idx_df_inventory_cold_storage_telemetry_02_rest_branch 
ON df_inventory_cold_storage_telemetry_02(restaurant_id, branch_id);

CREATE TABLE IF NOT EXISTS df_inventory_cold_storage_telemetry_03 (
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

CREATE INDEX IF NOT EXISTS idx_df_inventory_cold_storage_telemetry_03_rest_branch 
ON df_inventory_cold_storage_telemetry_03(restaurant_id, branch_id);

CREATE TABLE IF NOT EXISTS df_inventory_cold_storage_telemetry_04 (
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

CREATE INDEX IF NOT EXISTS idx_df_inventory_cold_storage_telemetry_04_rest_branch 
ON df_inventory_cold_storage_telemetry_04(restaurant_id, branch_id);

CREATE TABLE IF NOT EXISTS df_inventory_cold_storage_telemetry_05 (
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

CREATE INDEX IF NOT EXISTS idx_df_inventory_cold_storage_telemetry_05_rest_branch 
ON df_inventory_cold_storage_telemetry_05(restaurant_id, branch_id);

CREATE TABLE IF NOT EXISTS df_inventory_cold_storage_telemetry_06 (
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

CREATE INDEX IF NOT EXISTS idx_df_inventory_cold_storage_telemetry_06_rest_branch 
ON df_inventory_cold_storage_telemetry_06(restaurant_id, branch_id);

CREATE TABLE IF NOT EXISTS df_inventory_cold_storage_telemetry_07 (
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

CREATE INDEX IF NOT EXISTS idx_df_inventory_cold_storage_telemetry_07_rest_branch 
ON df_inventory_cold_storage_telemetry_07(restaurant_id, branch_id);

CREATE TABLE IF NOT EXISTS df_inventory_cold_storage_telemetry_08 (
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

CREATE INDEX IF NOT EXISTS idx_df_inventory_cold_storage_telemetry_08_rest_branch 
ON df_inventory_cold_storage_telemetry_08(restaurant_id, branch_id);

CREATE TABLE IF NOT EXISTS df_inventory_cold_storage_telemetry_09 (
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

CREATE INDEX IF NOT EXISTS idx_df_inventory_cold_storage_telemetry_09_rest_branch 
ON df_inventory_cold_storage_telemetry_09(restaurant_id, branch_id);

CREATE TABLE IF NOT EXISTS df_inventory_cold_storage_telemetry_10 (
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

CREATE INDEX IF NOT EXISTS idx_df_inventory_cold_storage_telemetry_10_rest_branch 
ON df_inventory_cold_storage_telemetry_10(restaurant_id, branch_id);

CREATE TABLE IF NOT EXISTS df_inventory_cold_storage_telemetry_11 (
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

CREATE INDEX IF NOT EXISTS idx_df_inventory_cold_storage_telemetry_11_rest_branch 
ON df_inventory_cold_storage_telemetry_11(restaurant_id, branch_id);

CREATE TABLE IF NOT EXISTS df_inventory_cold_storage_telemetry_12 (
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

CREATE INDEX IF NOT EXISTS idx_df_inventory_cold_storage_telemetry_12_rest_branch 
ON df_inventory_cold_storage_telemetry_12(restaurant_id, branch_id);

CREATE TABLE IF NOT EXISTS df_inventory_cold_storage_telemetry_13 (
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

CREATE INDEX IF NOT EXISTS idx_df_inventory_cold_storage_telemetry_13_rest_branch 
ON df_inventory_cold_storage_telemetry_13(restaurant_id, branch_id);

CREATE TABLE IF NOT EXISTS df_inventory_cold_storage_telemetry_14 (
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

CREATE INDEX IF NOT EXISTS idx_df_inventory_cold_storage_telemetry_14_rest_branch 
ON df_inventory_cold_storage_telemetry_14(restaurant_id, branch_id);

CREATE TABLE IF NOT EXISTS df_inventory_cold_storage_telemetry_15 (
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

CREATE INDEX IF NOT EXISTS idx_df_inventory_cold_storage_telemetry_15_rest_branch 
ON df_inventory_cold_storage_telemetry_15(restaurant_id, branch_id);

CREATE TABLE IF NOT EXISTS df_inventory_cold_storage_telemetry_16 (
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

CREATE INDEX IF NOT EXISTS idx_df_inventory_cold_storage_telemetry_16_rest_branch 
ON df_inventory_cold_storage_telemetry_16(restaurant_id, branch_id);

CREATE TABLE IF NOT EXISTS df_inventory_cold_storage_telemetry_17 (
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

CREATE INDEX IF NOT EXISTS idx_df_inventory_cold_storage_telemetry_17_rest_branch 
ON df_inventory_cold_storage_telemetry_17(restaurant_id, branch_id);

CREATE TABLE IF NOT EXISTS df_inventory_cold_storage_telemetry_18 (
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

CREATE INDEX IF NOT EXISTS idx_df_inventory_cold_storage_telemetry_18_rest_branch 
ON df_inventory_cold_storage_telemetry_18(restaurant_id, branch_id);

CREATE TABLE IF NOT EXISTS df_inventory_cold_storage_telemetry_19 (
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

CREATE INDEX IF NOT EXISTS idx_df_inventory_cold_storage_telemetry_19_rest_branch 
ON df_inventory_cold_storage_telemetry_19(restaurant_id, branch_id);

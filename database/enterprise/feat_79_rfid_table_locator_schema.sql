-- DineFlow Enterprise Schema Extension
-- Feature: RFID Guest Table Locator for Fast-Casual Food Runners (rfid-table-locator)
-- Optimized for PostgreSQL and SQLite Compatibility

CREATE TABLE IF NOT EXISTS df_tables_rfid_table_locator_01 (
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

CREATE INDEX IF NOT EXISTS idx_df_tables_rfid_table_locator_01_rest_branch 
ON df_tables_rfid_table_locator_01(restaurant_id, branch_id);

CREATE TABLE IF NOT EXISTS df_tables_rfid_table_locator_02 (
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

CREATE INDEX IF NOT EXISTS idx_df_tables_rfid_table_locator_02_rest_branch 
ON df_tables_rfid_table_locator_02(restaurant_id, branch_id);

CREATE TABLE IF NOT EXISTS df_tables_rfid_table_locator_03 (
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

CREATE INDEX IF NOT EXISTS idx_df_tables_rfid_table_locator_03_rest_branch 
ON df_tables_rfid_table_locator_03(restaurant_id, branch_id);

CREATE TABLE IF NOT EXISTS df_tables_rfid_table_locator_04 (
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

CREATE INDEX IF NOT EXISTS idx_df_tables_rfid_table_locator_04_rest_branch 
ON df_tables_rfid_table_locator_04(restaurant_id, branch_id);

CREATE TABLE IF NOT EXISTS df_tables_rfid_table_locator_05 (
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

CREATE INDEX IF NOT EXISTS idx_df_tables_rfid_table_locator_05_rest_branch 
ON df_tables_rfid_table_locator_05(restaurant_id, branch_id);

CREATE TABLE IF NOT EXISTS df_tables_rfid_table_locator_06 (
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

CREATE INDEX IF NOT EXISTS idx_df_tables_rfid_table_locator_06_rest_branch 
ON df_tables_rfid_table_locator_06(restaurant_id, branch_id);

CREATE TABLE IF NOT EXISTS df_tables_rfid_table_locator_07 (
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

CREATE INDEX IF NOT EXISTS idx_df_tables_rfid_table_locator_07_rest_branch 
ON df_tables_rfid_table_locator_07(restaurant_id, branch_id);

CREATE TABLE IF NOT EXISTS df_tables_rfid_table_locator_08 (
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

CREATE INDEX IF NOT EXISTS idx_df_tables_rfid_table_locator_08_rest_branch 
ON df_tables_rfid_table_locator_08(restaurant_id, branch_id);

CREATE TABLE IF NOT EXISTS df_tables_rfid_table_locator_09 (
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

CREATE INDEX IF NOT EXISTS idx_df_tables_rfid_table_locator_09_rest_branch 
ON df_tables_rfid_table_locator_09(restaurant_id, branch_id);

CREATE TABLE IF NOT EXISTS df_tables_rfid_table_locator_10 (
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

CREATE INDEX IF NOT EXISTS idx_df_tables_rfid_table_locator_10_rest_branch 
ON df_tables_rfid_table_locator_10(restaurant_id, branch_id);

CREATE TABLE IF NOT EXISTS df_tables_rfid_table_locator_11 (
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

CREATE INDEX IF NOT EXISTS idx_df_tables_rfid_table_locator_11_rest_branch 
ON df_tables_rfid_table_locator_11(restaurant_id, branch_id);

CREATE TABLE IF NOT EXISTS df_tables_rfid_table_locator_12 (
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

CREATE INDEX IF NOT EXISTS idx_df_tables_rfid_table_locator_12_rest_branch 
ON df_tables_rfid_table_locator_12(restaurant_id, branch_id);

CREATE TABLE IF NOT EXISTS df_tables_rfid_table_locator_13 (
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

CREATE INDEX IF NOT EXISTS idx_df_tables_rfid_table_locator_13_rest_branch 
ON df_tables_rfid_table_locator_13(restaurant_id, branch_id);

CREATE TABLE IF NOT EXISTS df_tables_rfid_table_locator_14 (
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

CREATE INDEX IF NOT EXISTS idx_df_tables_rfid_table_locator_14_rest_branch 
ON df_tables_rfid_table_locator_14(restaurant_id, branch_id);

CREATE TABLE IF NOT EXISTS df_tables_rfid_table_locator_15 (
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

CREATE INDEX IF NOT EXISTS idx_df_tables_rfid_table_locator_15_rest_branch 
ON df_tables_rfid_table_locator_15(restaurant_id, branch_id);

CREATE TABLE IF NOT EXISTS df_tables_rfid_table_locator_16 (
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

CREATE INDEX IF NOT EXISTS idx_df_tables_rfid_table_locator_16_rest_branch 
ON df_tables_rfid_table_locator_16(restaurant_id, branch_id);

CREATE TABLE IF NOT EXISTS df_tables_rfid_table_locator_17 (
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

CREATE INDEX IF NOT EXISTS idx_df_tables_rfid_table_locator_17_rest_branch 
ON df_tables_rfid_table_locator_17(restaurant_id, branch_id);

CREATE TABLE IF NOT EXISTS df_tables_rfid_table_locator_18 (
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

CREATE INDEX IF NOT EXISTS idx_df_tables_rfid_table_locator_18_rest_branch 
ON df_tables_rfid_table_locator_18(restaurant_id, branch_id);

CREATE TABLE IF NOT EXISTS df_tables_rfid_table_locator_19 (
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

CREATE INDEX IF NOT EXISTS idx_df_tables_rfid_table_locator_19_rest_branch 
ON df_tables_rfid_table_locator_19(restaurant_id, branch_id);

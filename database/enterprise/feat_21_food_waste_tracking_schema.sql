-- DineFlow Enterprise Schema Extension
-- Feature: Kitchen Prep Waste, Spoilage, and Audit Disposal Log (food-waste-tracking)
-- Optimized for PostgreSQL and SQLite Compatibility

CREATE TABLE IF NOT EXISTS df_inventory_food_waste_tracking_01 (
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

CREATE INDEX IF NOT EXISTS idx_df_inventory_food_waste_tracking_01_rest_branch 
ON df_inventory_food_waste_tracking_01(restaurant_id, branch_id);

CREATE TABLE IF NOT EXISTS df_inventory_food_waste_tracking_02 (
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

CREATE INDEX IF NOT EXISTS idx_df_inventory_food_waste_tracking_02_rest_branch 
ON df_inventory_food_waste_tracking_02(restaurant_id, branch_id);

CREATE TABLE IF NOT EXISTS df_inventory_food_waste_tracking_03 (
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

CREATE INDEX IF NOT EXISTS idx_df_inventory_food_waste_tracking_03_rest_branch 
ON df_inventory_food_waste_tracking_03(restaurant_id, branch_id);

CREATE TABLE IF NOT EXISTS df_inventory_food_waste_tracking_04 (
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

CREATE INDEX IF NOT EXISTS idx_df_inventory_food_waste_tracking_04_rest_branch 
ON df_inventory_food_waste_tracking_04(restaurant_id, branch_id);

CREATE TABLE IF NOT EXISTS df_inventory_food_waste_tracking_05 (
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

CREATE INDEX IF NOT EXISTS idx_df_inventory_food_waste_tracking_05_rest_branch 
ON df_inventory_food_waste_tracking_05(restaurant_id, branch_id);

CREATE TABLE IF NOT EXISTS df_inventory_food_waste_tracking_06 (
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

CREATE INDEX IF NOT EXISTS idx_df_inventory_food_waste_tracking_06_rest_branch 
ON df_inventory_food_waste_tracking_06(restaurant_id, branch_id);

CREATE TABLE IF NOT EXISTS df_inventory_food_waste_tracking_07 (
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

CREATE INDEX IF NOT EXISTS idx_df_inventory_food_waste_tracking_07_rest_branch 
ON df_inventory_food_waste_tracking_07(restaurant_id, branch_id);

CREATE TABLE IF NOT EXISTS df_inventory_food_waste_tracking_08 (
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

CREATE INDEX IF NOT EXISTS idx_df_inventory_food_waste_tracking_08_rest_branch 
ON df_inventory_food_waste_tracking_08(restaurant_id, branch_id);

CREATE TABLE IF NOT EXISTS df_inventory_food_waste_tracking_09 (
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

CREATE INDEX IF NOT EXISTS idx_df_inventory_food_waste_tracking_09_rest_branch 
ON df_inventory_food_waste_tracking_09(restaurant_id, branch_id);

CREATE TABLE IF NOT EXISTS df_inventory_food_waste_tracking_10 (
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

CREATE INDEX IF NOT EXISTS idx_df_inventory_food_waste_tracking_10_rest_branch 
ON df_inventory_food_waste_tracking_10(restaurant_id, branch_id);

CREATE TABLE IF NOT EXISTS df_inventory_food_waste_tracking_11 (
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

CREATE INDEX IF NOT EXISTS idx_df_inventory_food_waste_tracking_11_rest_branch 
ON df_inventory_food_waste_tracking_11(restaurant_id, branch_id);

CREATE TABLE IF NOT EXISTS df_inventory_food_waste_tracking_12 (
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

CREATE INDEX IF NOT EXISTS idx_df_inventory_food_waste_tracking_12_rest_branch 
ON df_inventory_food_waste_tracking_12(restaurant_id, branch_id);

CREATE TABLE IF NOT EXISTS df_inventory_food_waste_tracking_13 (
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

CREATE INDEX IF NOT EXISTS idx_df_inventory_food_waste_tracking_13_rest_branch 
ON df_inventory_food_waste_tracking_13(restaurant_id, branch_id);

CREATE TABLE IF NOT EXISTS df_inventory_food_waste_tracking_14 (
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

CREATE INDEX IF NOT EXISTS idx_df_inventory_food_waste_tracking_14_rest_branch 
ON df_inventory_food_waste_tracking_14(restaurant_id, branch_id);

CREATE TABLE IF NOT EXISTS df_inventory_food_waste_tracking_15 (
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

CREATE INDEX IF NOT EXISTS idx_df_inventory_food_waste_tracking_15_rest_branch 
ON df_inventory_food_waste_tracking_15(restaurant_id, branch_id);

CREATE TABLE IF NOT EXISTS df_inventory_food_waste_tracking_16 (
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

CREATE INDEX IF NOT EXISTS idx_df_inventory_food_waste_tracking_16_rest_branch 
ON df_inventory_food_waste_tracking_16(restaurant_id, branch_id);

CREATE TABLE IF NOT EXISTS df_inventory_food_waste_tracking_17 (
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

CREATE INDEX IF NOT EXISTS idx_df_inventory_food_waste_tracking_17_rest_branch 
ON df_inventory_food_waste_tracking_17(restaurant_id, branch_id);

CREATE TABLE IF NOT EXISTS df_inventory_food_waste_tracking_18 (
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

CREATE INDEX IF NOT EXISTS idx_df_inventory_food_waste_tracking_18_rest_branch 
ON df_inventory_food_waste_tracking_18(restaurant_id, branch_id);

CREATE TABLE IF NOT EXISTS df_inventory_food_waste_tracking_19 (
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

CREATE INDEX IF NOT EXISTS idx_df_inventory_food_waste_tracking_19_rest_branch 
ON df_inventory_food_waste_tracking_19(restaurant_id, branch_id);

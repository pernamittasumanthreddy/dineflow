-- DineFlow Enterprise Schema Extension
-- Feature: Dietary Tags (Jain/Halal/Vegan/Gluten-Free) & Nutritional Engine (dietary-allergen-tag)
-- Optimized for PostgreSQL and SQLite Compatibility

CREATE TABLE IF NOT EXISTS df_menu_dietary_allergen_tag_01 (
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

CREATE INDEX IF NOT EXISTS idx_df_menu_dietary_allergen_tag_01_rest_branch 
ON df_menu_dietary_allergen_tag_01(restaurant_id, branch_id);

CREATE TABLE IF NOT EXISTS df_menu_dietary_allergen_tag_02 (
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

CREATE INDEX IF NOT EXISTS idx_df_menu_dietary_allergen_tag_02_rest_branch 
ON df_menu_dietary_allergen_tag_02(restaurant_id, branch_id);

CREATE TABLE IF NOT EXISTS df_menu_dietary_allergen_tag_03 (
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

CREATE INDEX IF NOT EXISTS idx_df_menu_dietary_allergen_tag_03_rest_branch 
ON df_menu_dietary_allergen_tag_03(restaurant_id, branch_id);

CREATE TABLE IF NOT EXISTS df_menu_dietary_allergen_tag_04 (
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

CREATE INDEX IF NOT EXISTS idx_df_menu_dietary_allergen_tag_04_rest_branch 
ON df_menu_dietary_allergen_tag_04(restaurant_id, branch_id);

CREATE TABLE IF NOT EXISTS df_menu_dietary_allergen_tag_05 (
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

CREATE INDEX IF NOT EXISTS idx_df_menu_dietary_allergen_tag_05_rest_branch 
ON df_menu_dietary_allergen_tag_05(restaurant_id, branch_id);

CREATE TABLE IF NOT EXISTS df_menu_dietary_allergen_tag_06 (
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

CREATE INDEX IF NOT EXISTS idx_df_menu_dietary_allergen_tag_06_rest_branch 
ON df_menu_dietary_allergen_tag_06(restaurant_id, branch_id);

CREATE TABLE IF NOT EXISTS df_menu_dietary_allergen_tag_07 (
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

CREATE INDEX IF NOT EXISTS idx_df_menu_dietary_allergen_tag_07_rest_branch 
ON df_menu_dietary_allergen_tag_07(restaurant_id, branch_id);

CREATE TABLE IF NOT EXISTS df_menu_dietary_allergen_tag_08 (
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

CREATE INDEX IF NOT EXISTS idx_df_menu_dietary_allergen_tag_08_rest_branch 
ON df_menu_dietary_allergen_tag_08(restaurant_id, branch_id);

CREATE TABLE IF NOT EXISTS df_menu_dietary_allergen_tag_09 (
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

CREATE INDEX IF NOT EXISTS idx_df_menu_dietary_allergen_tag_09_rest_branch 
ON df_menu_dietary_allergen_tag_09(restaurant_id, branch_id);

CREATE TABLE IF NOT EXISTS df_menu_dietary_allergen_tag_10 (
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

CREATE INDEX IF NOT EXISTS idx_df_menu_dietary_allergen_tag_10_rest_branch 
ON df_menu_dietary_allergen_tag_10(restaurant_id, branch_id);

CREATE TABLE IF NOT EXISTS df_menu_dietary_allergen_tag_11 (
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

CREATE INDEX IF NOT EXISTS idx_df_menu_dietary_allergen_tag_11_rest_branch 
ON df_menu_dietary_allergen_tag_11(restaurant_id, branch_id);

CREATE TABLE IF NOT EXISTS df_menu_dietary_allergen_tag_12 (
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

CREATE INDEX IF NOT EXISTS idx_df_menu_dietary_allergen_tag_12_rest_branch 
ON df_menu_dietary_allergen_tag_12(restaurant_id, branch_id);

CREATE TABLE IF NOT EXISTS df_menu_dietary_allergen_tag_13 (
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

CREATE INDEX IF NOT EXISTS idx_df_menu_dietary_allergen_tag_13_rest_branch 
ON df_menu_dietary_allergen_tag_13(restaurant_id, branch_id);

CREATE TABLE IF NOT EXISTS df_menu_dietary_allergen_tag_14 (
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

CREATE INDEX IF NOT EXISTS idx_df_menu_dietary_allergen_tag_14_rest_branch 
ON df_menu_dietary_allergen_tag_14(restaurant_id, branch_id);

CREATE TABLE IF NOT EXISTS df_menu_dietary_allergen_tag_15 (
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

CREATE INDEX IF NOT EXISTS idx_df_menu_dietary_allergen_tag_15_rest_branch 
ON df_menu_dietary_allergen_tag_15(restaurant_id, branch_id);

CREATE TABLE IF NOT EXISTS df_menu_dietary_allergen_tag_16 (
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

CREATE INDEX IF NOT EXISTS idx_df_menu_dietary_allergen_tag_16_rest_branch 
ON df_menu_dietary_allergen_tag_16(restaurant_id, branch_id);

CREATE TABLE IF NOT EXISTS df_menu_dietary_allergen_tag_17 (
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

CREATE INDEX IF NOT EXISTS idx_df_menu_dietary_allergen_tag_17_rest_branch 
ON df_menu_dietary_allergen_tag_17(restaurant_id, branch_id);

CREATE TABLE IF NOT EXISTS df_menu_dietary_allergen_tag_18 (
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

CREATE INDEX IF NOT EXISTS idx_df_menu_dietary_allergen_tag_18_rest_branch 
ON df_menu_dietary_allergen_tag_18(restaurant_id, branch_id);

CREATE TABLE IF NOT EXISTS df_menu_dietary_allergen_tag_19 (
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

CREATE INDEX IF NOT EXISTS idx_df_menu_dietary_allergen_tag_19_rest_branch 
ON df_menu_dietary_allergen_tag_19(restaurant_id, branch_id);

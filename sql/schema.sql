-- GrowthIQ Relational Database Schema
-- SQLite 3 DDL with Foreign Key Enforcement, Check Constraints, and Indexes

PRAGMA foreign_keys = ON;

-- 1. Product Categories
CREATE TABLE IF NOT EXISTS product_categories (
    category TEXT PRIMARY KEY,
    sku_count INTEGER NOT NULL CHECK(sku_count >= 0),
    avg_price_inr REAL NOT NULL CHECK(avg_price_inr >= 0),
    avg_gross_margin REAL NOT NULL CHECK(avg_gross_margin >= 0 AND avg_gross_margin <= 1),
    department TEXT NOT NULL
);

-- 2. Products Catalogue
CREATE TABLE IF NOT EXISTS products (
    product_id TEXT PRIMARY KEY,
    product_name TEXT NOT NULL,
    category TEXT NOT NULL,
    target_gender TEXT NOT NULL,
    list_price_inr REAL NOT NULL CHECK(list_price_inr > 0),
    unit_cost_inr REAL NOT NULL CHECK(unit_cost_inr > 0),
    gross_margin_rate REAL NOT NULL CHECK(gross_margin_rate >= 0 AND gross_margin_rate <= 1),
    FOREIGN KEY(category) REFERENCES product_categories(category)
);

-- 3. Customer Demographic Profiles
CREATE TABLE IF NOT EXISTS customers (
    customer_id TEXT PRIMARY KEY,
    signup_date TEXT NOT NULL,
    city TEXT NOT NULL,
    age INTEGER NOT NULL CHECK(age >= 16 AND age <= 100),
    persona_seed TEXT NOT NULL
);

-- 4. Marketing Campaigns Metadata
CREATE TABLE IF NOT EXISTS campaigns (
    campaign TEXT PRIMARY KEY,
    channel TEXT NOT NULL,
    campaign_type TEXT NOT NULL,
    expected_cvr REAL,
    target_cpc REAL,
    target_cpm REAL
);

-- 5. Campaign Daily Expenditure & Performance
CREATE TABLE IF NOT EXISTS campaign_spend (
    spend_id INTEGER PRIMARY KEY AUTOINCREMENT,
    spend_date TEXT NOT NULL,
    channel TEXT NOT NULL,
    campaign TEXT NOT NULL,
    spend_inr REAL NOT NULL CHECK(spend_inr >= 0),
    impressions INTEGER NOT NULL CHECK(impressions >= 0),
    clicks INTEGER NOT NULL CHECK(clicks >= 0),
    FOREIGN KEY(campaign) REFERENCES campaigns(campaign)
);

-- 6. Website Sessions
CREATE TABLE IF NOT EXISTS sessions (
    session_id TEXT PRIMARY KEY,
    session_date TEXT NOT NULL,
    customer_id TEXT,
    channel TEXT NOT NULL,
    campaign TEXT NOT NULL,
    device TEXT NOT NULL,
    landing_page TEXT NOT NULL,
    session_cost_inr REAL NOT NULL DEFAULT 0.0 CHECK(session_cost_inr >= 0),
    FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
);

-- 7. Funnel Website Events
CREATE TABLE IF NOT EXISTS events (
    event_id TEXT PRIMARY KEY,
    session_id TEXT NOT NULL,
    event_timestamp TEXT NOT NULL,
    event_name TEXT NOT NULL,
    FOREIGN KEY(session_id) REFERENCES sessions(session_id)
);

-- 8. Orders
CREATE TABLE IF NOT EXISTS orders (
    order_id TEXT PRIMARY KEY,
    customer_id TEXT NOT NULL,
    session_id TEXT NOT NULL,
    order_date TEXT NOT NULL,
    channel TEXT NOT NULL,
    campaign TEXT NOT NULL,
    device TEXT NOT NULL,
    discount_rate REAL NOT NULL DEFAULT 0.0 CHECK(discount_rate >= 0 AND discount_rate <= 1),
    order_status TEXT NOT NULL,
    FOREIGN KEY(customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY(session_id) REFERENCES sessions(session_id)
);

-- 9. Order Items (Line Items)
CREATE TABLE IF NOT EXISTS order_items (
    item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id TEXT NOT NULL,
    product_id TEXT NOT NULL,
    quantity INTEGER NOT NULL CHECK(quantity > 0),
    list_unit_price_inr REAL NOT NULL CHECK(list_unit_price_inr >= 0),
    selling_unit_price_inr REAL NOT NULL CHECK(selling_unit_price_inr >= 0),
    line_gross_profit_inr REAL NOT NULL,
    FOREIGN KEY(order_id) REFERENCES orders(order_id),
    FOREIGN KEY(product_id) REFERENCES products(product_id)
);

-- 10. Inventory Snapshot
CREATE TABLE IF NOT EXISTS inventory (
    product_id TEXT PRIMARY KEY,
    on_hand_units INTEGER NOT NULL CHECK(on_hand_units >= 0),
    reorder_point_units INTEGER NOT NULL CHECK(reorder_point_units >= 0),
    safety_stock_units INTEGER NOT NULL CHECK(safety_stock_units >= 0),
    lead_time_days INTEGER NOT NULL CHECK(lead_time_days > 0),
    snapshot_date TEXT NOT NULL,
    FOREIGN KEY(product_id) REFERENCES products(product_id)
);

-- Performance Indexes
CREATE INDEX IF NOT EXISTS idx_sessions_date ON sessions(session_date);
CREATE INDEX IF NOT EXISTS idx_sessions_channel ON sessions(channel);
CREATE INDEX IF NOT EXISTS idx_orders_date ON orders(order_date);
CREATE INDEX IF NOT EXISTS idx_orders_customer ON orders(customer_id);
CREATE INDEX IF NOT EXISTS idx_orders_channel ON orders(channel);
CREATE INDEX IF NOT EXISTS idx_order_items_order ON order_items(order_id);
CREATE INDEX IF NOT EXISTS idx_order_items_product ON order_items(product_id);
CREATE INDEX IF NOT EXISTS idx_events_session ON events(session_id);
CREATE INDEX IF NOT EXISTS idx_spend_date ON campaign_spend(spend_date);

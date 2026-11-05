# GrowthIQ — Data Dictionary

This document specifies the schema, grain, primary keys, foreign keys, and column-level definitions for all 10 interconnected tables comprising the GrowthIQ analytics platform.

All datasets represent synthetic fashion and athleisure e-commerce activity for calendar year 2025 (2025-01-01 to 2025-12-31).

---

## 1. `product_categories`
- **Grain:** One row per merchandise category.
- **Primary Key:** `category`
- **Description:** Merchandise classification hierarchy grouping individual SKUs.

| Column | Data Type | Constraint | Description | Example |
|---|---|---|---|---|
| `category` | TEXT | PRIMARY KEY | Unique name of the merchandise category | `Leggings` |
| `sku_count` | INTEGER | NOT NULL, >= 0 | Number of distinct active SKUs in the category | `3` |
| `avg_price_inr` | REAL | NOT NULL, >= 0 | Average catalogue list price in Indian Rupees (INR) | `2499.0` |
| `avg_gross_margin` | REAL | NOT NULL, [0, 1] | Target category-wide gross margin percentage | `0.67` |
| `department` | TEXT | NOT NULL | High-level department grouping | `Activewear` |

---

## 2. `products`
- **Grain:** One row per individual stock keeping unit (SKU).
- **Primary Key:** `product_id`
- **Foreign Key:** `category` references `product_categories(category)`
- **Description:** Athleisure product catalogue containing pricing, unit costs, and merchandising metadata.

| Column | Data Type | Constraint | Description | Example |
|---|---|---|---|---|
| `product_id` | TEXT | PRIMARY KEY | Unique product identifier code | `P001` |
| `product_name` | TEXT | NOT NULL | Commercial product title | `Contour Seamless Leggings` |
| `category` | TEXT | FOREIGN KEY | Associated merchandise category | `Leggings` |
| `target_gender` | TEXT | NOT NULL | Primary target demographic | `Women` |
| `list_price_inr` | REAL | NOT NULL, > 0 | Recommended retail list price (INR) | `2499.0` |
| `unit_cost_inr` | REAL | NOT NULL, > 0 | Cost of goods sold (COGS) per unit (INR) | `850.0` |
| `gross_margin_rate`| REAL | NOT NULL, [0, 1] | Theoretical gross margin at full retail list price | `0.66` |

---

## 3. `customers`
- **Grain:** One row per registered customer.
- **Primary Key:** `customer_id`
- **Description:** Customer demographic profiles across Indian metro cities.

| Column | Data Type | Constraint | Description | Example |
|---|---|---|---|---|
| `customer_id` | TEXT | PRIMARY KEY | Unique customer account identifier | `CUST00124` |
| `signup_date` | TEXT (ISO) | NOT NULL | Account creation date (YYYY-MM-DD) | `2025-02-14` |
| `city` | TEXT | NOT NULL | Primary residential metro city in India | `Bengaluru` |
| `age` | INTEGER | NOT NULL, [16, 100]| Customer age in years | `28` |
| `persona_seed` | TEXT | NOT NULL | Algorithmic behavioral archetype seed | `Fitness Enthusiast` |

---

## 4. `campaigns`
- **Grain:** One row per marketing campaign initiative.
- **Primary Key:** `campaign`
- **Description:** Campaign metadata across paid and organic acquisition channels.

| Column | Data Type | Constraint | Description | Example |
|---|---|---|---|---|
| `campaign` | TEXT | PRIMARY KEY | Unique campaign identifier name | `Meta_Spring_Sculpt` |
| `channel` | TEXT | NOT NULL | Acquisition channel name | `Paid Social` |
| `campaign_type` | TEXT | NOT NULL | Strategic intent (Prospecting, Brand, Retargeting) | `Prospecting` |
| `expected_cvr` | REAL | Nullable | Benchmark expected conversion rate | `0.024` |
| `target_cpc` | REAL | Nullable | Benchmark target cost per click (INR) | `22.0` |
| `target_cpm` | REAL | Nullable | Benchmark target cost per mille impressions (INR) | `480.0` |

---

## 5. `campaign_spend`
- **Grain:** One row per day per campaign.
- **Primary Key:** `spend_id` (Autoincrement)
- **Foreign Key:** `campaign` references `campaigns(campaign)`
- **Description:** Daily advertising expenditures, delivered impressions, and click engagements.

| Column | Data Type | Constraint | Description | Example |
|---|---|---|---|---|
| `spend_id` | INTEGER | PRIMARY KEY | Auto-generated row ID | `1` |
| `spend_date` | TEXT (ISO) | NOT NULL | Calendar date of media spend (YYYY-MM-DD) | `2025-03-01` |
| `channel` | TEXT | NOT NULL | Marketing channel | `Paid Social` |
| `campaign` | TEXT | FOREIGN KEY | Name of advertising campaign | `Meta_Spring_Sculpt` |
| `spend_inr` | REAL | NOT NULL, >= 0 | Media budget outlay in Indian Rupees (INR) | `1124.50` |
| `impressions` | INTEGER | NOT NULL, >= 0 | Total advertising impressions served | `2340` |
| `clicks` | INTEGER | NOT NULL, >= 0 | Total paid link click events | `48` |

---

## 6. `sessions`
- **Grain:** One row per browsing session visit.
- **Primary Key:** `session_id`
- **Foreign Key:** `customer_id` references `customers(customer_id)` (Nullable for guest visitors)
- **Description:** Web telemetry recording visitor entry points, traffic channels, and device types.

| Column | Data Type | Constraint | Description | Example |
|---|---|---|---|---|
| `session_id` | TEXT | PRIMARY KEY | Unique browsing session identifier | `SESS0001428` |
| `session_date` | TEXT (ISO) | NOT NULL | Date of session visit (YYYY-MM-DD) | `2025-04-12` |
| `customer_id` | TEXT | FOREIGN KEY | Customer ID if authenticated/recognized | `CUST00412` |
| `channel` | TEXT | NOT NULL | Acquisition traffic channel | `Paid Social` |
| `campaign` | TEXT | NOT NULL | Campaign name parameter | `Meta_Spring_Sculpt` |
| `device` | TEXT | NOT NULL | Client device category (`Mobile`, `Desktop`, `Tablet`) | `Mobile` |
| `landing_page` | TEXT | NOT NULL | Initial URI path entered by visitor | `/collections/leggings` |
| `session_cost_inr` | REAL | NOT NULL, >= 0 | Simulated attribution cost proxy for session (INR) | `24.50` |

---

## 7. `events`
- **Grain:** One row per interaction event within a session.
- **Primary Key:** `event_id`
- **Foreign Key:** `session_id` references `sessions(session_id)`
- **Description:** Granular e-commerce milestone event telemetry modeled on Google Analytics 4 (GA4).

| Column | Data Type | Constraint | Description | Example |
|---|---|---|---|---|
| `event_id` | TEXT | PRIMARY KEY | Unique event identifier | `EVT00021481` |
| `session_id` | TEXT | FOREIGN KEY | Parent session ID | `SESS0001428` |
| `event_timestamp`| TEXT (ISO) | NOT NULL | Monotonic ISO timestamp (YYYY-MM-DD HH:MM:SS) | `2025-04-12 14:22:10` |
| `event_name` | TEXT | NOT NULL | Standardized milestone action (`session_start`, `view_item`, `add_to_cart`, `begin_checkout`, `purchase`) | `add_to_cart` |

---

## 8. `orders`
- **Grain:** One row per customer order transaction.
- **Primary Key:** `order_id`
- **Foreign Keys:**
  - `customer_id` references `customers(customer_id)`
  - `session_id` references `sessions(session_id)`
- **Description:** Commercial header record capturing order placement date, channel, and discount rate.

| Column | Data Type | Constraint | Description | Example |
|---|---|---|---|---|
| `order_id` | TEXT | PRIMARY KEY | Unique customer order identifier | `ORD000412` |
| `customer_id` | TEXT | FOREIGN KEY | Purchasing customer account | `CUST00412` |
| `session_id` | TEXT | FOREIGN KEY | Converting web session | `SESS0001428` |
| `order_date` | TEXT (ISO) | NOT NULL | Order date (YYYY-MM-DD) | `2025-04-12` |
| `channel` | TEXT | NOT NULL | Converting acquisition channel (Last-Touch) | `Paid Social` |
| `campaign` | TEXT | NOT NULL | Converting campaign | `Meta_Spring_Sculpt` |
| `device` | TEXT | NOT NULL | Device used to complete transaction | `Mobile` |
| `discount_rate` | REAL | NOT NULL, [0, 1] | Order-level promotional discount percentage | `0.10` |
| `order_status` | TEXT | NOT NULL | Fulfillment state (`Completed`, `Refunded`, `Cancelled`)| `Completed` |

---

## 9. `order_items`
- **Grain:** One row per SKU purchased within an order.
- **Primary Key:** `item_id` (Autoincrement)
- **Foreign Keys:**
  - `order_id` references `orders(order_id)`
  - `product_id` references `products(product_id)`
- **Description:** Line-item transaction grain capturing quantity, selling price, and realized gross profit.

| Column | Data Type | Constraint | Description | Example |
|---|---|---|---|---|
| `item_id` | INTEGER | PRIMARY KEY | Auto-generated row ID | `1` |
| `order_id` | TEXT | FOREIGN KEY | Parent order identifier | `ORD000412` |
| `product_id` | TEXT | FOREIGN KEY | Purchased SKU identifier | `P001` |
| `quantity` | INTEGER | NOT NULL, > 0 | Units ordered | `1` |
| `list_unit_price_inr` | REAL | NOT NULL, >= 0 | List catalogue price prior to discount (INR) | `2499.0` |
| `selling_unit_price_inr` | REAL | NOT NULL, >= 0 | Realized selling price after line discount (INR) | `2249.10` |
| `line_gross_profit_inr` | REAL | NOT NULL | Gross profit: `(selling_price - unit_cost) * quantity` | `1399.10` |

---

## 10. `inventory`
- **Grain:** One row per product inventory snapshot.
- **Primary Key:** `product_id`
- **Foreign Key:** `product_id` references `products(product_id)`
- **Description:** Warehouse stock balance snapshot recording on-hand inventory and reorder triggers.

| Column | Data Type | Constraint | Description | Example |
|---|---|---|---|---|
| `product_id` | TEXT | PRIMARY KEY | Associated product SKU | `P001` |
| `on_hand_units` | INTEGER | NOT NULL, >= 0 | Physical stock currently in warehouse | `32` |
| `reorder_point_units` | INTEGER | NOT NULL, >= 0 | Stock level threshold triggering replenishment order | `50` |
| `safety_stock_units` | INTEGER | NOT NULL, >= 0 | Buffer stock threshold below which stockout risk is critical | `25` |
| `lead_time_days` | INTEGER | NOT NULL, > 0 | Supplier fulfillment lead time in days | `14` |
| `snapshot_date` | TEXT (ISO) | NOT NULL | Date inventory level was audited (YYYY-MM-DD) | `2025-12-31` |


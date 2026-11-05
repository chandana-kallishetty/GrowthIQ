-- GrowthIQ Analytical SQL Query Suite
-- Production-quality SQL queries covering Executive KPIs, Marketing Attribution,
-- RFM Segmentation, Cohort Retention, and Product Economics.

-- ============================================================================
-- QUERY 1: Executive Monthly Performance & MoM Revenue Growth
-- ============================================================================
WITH monthly_orders AS (
    SELECT
        strftime('%Y-%m', o.order_date) AS order_month,
        COUNT(DISTINCT o.order_id) AS total_orders,
        COUNT(DISTINCT o.customer_id) AS active_customers,
        SUM(oi.quantity * oi.selling_unit_price_inr) AS gross_revenue_inr,
        SUM(oi.line_gross_profit_inr) AS gross_profit_inr,
        SUM(oi.quantity) AS total_units_sold
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    WHERE o.order_status = 'Completed'
    GROUP BY strftime('%Y-%m', o.order_date)
)
SELECT
    order_month,
    total_orders,
    active_customers,
    total_units_sold,
    ROUND(gross_revenue_inr, 2) AS revenue_inr,
    ROUND(gross_revenue_inr / total_orders, 2) AS aov_inr,
    ROUND(gross_profit_inr, 2) AS gross_profit_inr,
    ROUND((gross_profit_inr / gross_revenue_inr) * 100, 2) AS gross_margin_pct,
    ROUND(
        ((gross_revenue_inr - LAG(gross_revenue_inr) OVER (ORDER BY order_month)) /
        LAG(gross_revenue_inr) OVER (ORDER BY order_month)) * 100,
        2
    ) AS mom_revenue_growth_pct
FROM monthly_orders
ORDER BY order_month;


-- ============================================================================
-- QUERY 2: Channel Efficiency, Blended ROAS, and Paid CAC
-- ============================================================================
WITH channel_spend AS (
    SELECT
        channel,
        SUM(spend_inr) AS total_spend_inr,
        SUM(impressions) AS total_impressions,
        SUM(clicks) AS total_clicks
    FROM campaign_spend
    GROUP BY channel
),
channel_sessions AS (
    SELECT
        channel,
        COUNT(DISTINCT session_id) AS total_sessions
    FROM sessions
    GROUP BY channel
),
channel_revenue AS (
    SELECT
        o.channel,
        COUNT(DISTINCT o.order_id) AS total_orders,
        COUNT(DISTINCT o.customer_id) AS unique_purchasers,
        SUM(oi.quantity * oi.selling_unit_price_inr) AS total_revenue_inr,
        SUM(oi.line_gross_profit_inr) AS total_gross_profit_inr
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    WHERE o.order_status = 'Completed'
    GROUP BY o.channel
)
SELECT
    cs.channel,
    COALESCE(cs.total_spend_inr, 0) AS spend_inr,
    COALESCE(sess.total_sessions, 0) AS sessions,
    COALESCE(cr.total_orders, 0) AS orders,
    COALESCE(cr.unique_purchasers, 0) AS customers,
    ROUND(COALESCE(cr.total_revenue_inr, 0), 2) AS revenue_inr,
    ROUND(COALESCE(cr.total_gross_profit_inr, 0), 2) AS gross_profit_inr,
    CASE
        WHEN COALESCE(cs.total_spend_inr, 0) > 0
        THEN ROUND(cr.total_revenue_inr / cs.total_spend_inr, 2)
        ELSE NULL
    END AS roas,
    CASE
        WHEN COALESCE(cr.unique_purchasers, 0) > 0 AND COALESCE(cs.total_spend_inr, 0) > 0
        THEN ROUND(cs.total_spend_inr / cr.unique_purchasers, 2)
        ELSE 0
    END AS cac_inr,
    CASE
        WHEN COALESCE(sess.total_sessions, 0) > 0
        THEN ROUND((CAST(cr.total_orders AS REAL) / sess.total_sessions) * 100, 2)
        ELSE 0
    END AS conversion_rate_pct
FROM channel_sessions sess
LEFT JOIN channel_spend cs ON sess.channel = cs.channel
LEFT JOIN channel_revenue cr ON sess.channel = cr.channel
ORDER BY revenue_inr DESC;


-- ============================================================================
-- QUERY 3: First-Touch vs. Last-Touch Marketing Attribution Comparison
-- ============================================================================
WITH customer_first_session AS (
    -- Identify the channel of the earliest recorded session for each customer
    SELECT
        customer_id,
        channel AS first_touch_channel,
        ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY session_date ASC, session_id ASC) AS rn
    FROM sessions
    WHERE customer_id IS NOT NULL
),
first_touch_map AS (
    SELECT customer_id, first_touch_channel
    FROM customer_first_session
    WHERE rn = 1
),
order_attributions AS (
    SELECT
        o.order_id,
        o.customer_id,
        ft.first_touch_channel,
        o.channel AS last_touch_channel,
        SUM(oi.quantity * oi.selling_unit_price_inr) AS order_revenue_inr
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    LEFT JOIN first_touch_map ft ON o.customer_id = ft.customer_id
    WHERE o.order_status = 'Completed'
    GROUP BY o.order_id, o.customer_id, ft.first_touch_channel, o.channel
),
first_touch_agg AS (
    SELECT
        first_touch_channel AS channel,
        COUNT(DISTINCT order_id) AS ft_orders,
        ROUND(SUM(order_revenue_inr), 2) AS ft_revenue_inr
    FROM order_attributions
    GROUP BY first_touch_channel
),
last_touch_agg AS (
    SELECT
        last_touch_channel AS channel,
        COUNT(DISTINCT order_id) AS lt_orders,
        ROUND(SUM(order_revenue_inr), 2) AS lt_revenue_inr
    FROM order_attributions
    GROUP BY last_touch_channel
)
SELECT
    COALESCE(lt.channel, ft.channel) AS channel,
    COALESCE(ft.ft_orders, 0) AS first_touch_orders,
    COALESCE(ft.ft_revenue_inr, 0) AS first_touch_revenue_inr,
    COALESCE(lt.lt_orders, 0) AS last_touch_orders,
    COALESCE(lt.lt_revenue_inr, 0) AS last_touch_revenue_inr,
    ROUND(COALESCE(lt.lt_revenue_inr, 0) - COALESCE(ft.ft_revenue_inr, 0), 2) AS lt_vs_ft_revenue_variance_inr
FROM last_touch_agg lt
FULL OUTER JOIN first_touch_agg ft ON lt.channel = ft.channel
ORDER BY last_touch_revenue_inr DESC;


-- ============================================================================
-- QUERY 4: RFM Customer Value Segmentation
-- ============================================================================
WITH customer_aggregates AS (
    SELECT
        o.customer_id,
        MAX(o.order_date) AS last_order_date,
        COUNT(DISTINCT o.order_id) AS frequency,
        SUM(oi.quantity * oi.selling_unit_price_inr) AS monetary_inr,
        CAST((julianday('2025-12-31') - julianday(MAX(o.order_date))) AS INTEGER) AS recency_days
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    WHERE o.order_status = 'Completed'
    GROUP BY o.customer_id
),
rfm_ranked AS (
    SELECT
        customer_id,
        recency_days,
        frequency,
        monetary_inr,
        NTILE(4) OVER (ORDER BY recency_days DESC) AS r_score, -- Lower recency days = higher score
        NTILE(4) OVER (ORDER BY frequency ASC) AS f_score,
        NTILE(4) OVER (ORDER BY monetary_inr ASC) AS m_score
    FROM customer_aggregates
)
SELECT
    customer_id,
    recency_days,
    frequency,
    ROUND(monetary_inr, 2) AS monetary_inr,
    r_score,
    f_score,
    m_score,
    CASE
        WHEN m_score = 4 AND f_score >= 3 THEN 'VIP Champions'
        WHEN f_score >= 3 THEN 'Loyal Customers'
        WHEN r_score >= 3 AND f_score = 1 THEN 'Promising Newcomers'
        WHEN r_score <= 2 AND f_score >= 2 THEN 'At-Risk High Value'
        WHEN r_score = 1 THEN 'Hibernating / Lapsed'
        ELSE 'Active Regulars'
    END AS customer_segment
FROM rfm_ranked;


-- ============================================================================
-- QUERY 5: Monthly Cohort Retention Triangle
-- ============================================================================
WITH customer_first_month AS (
    SELECT
        customer_id,
        MIN(strftime('%Y-%m', order_date)) AS cohort_month
    FROM orders
    WHERE order_status = 'Completed'
    GROUP BY customer_id
),
cohort_orders AS (
    SELECT
        o.customer_id,
        cfm.cohort_month,
        strftime('%Y-%m', o.order_date) AS order_month,
        (CAST(strftime('%Y', o.order_date) AS INTEGER) - CAST(substr(cfm.cohort_month, 1, 4) AS INTEGER)) * 12 +
        (CAST(strftime('%m', o.order_date) AS INTEGER) - CAST(substr(cfm.cohort_month, 6, 2) AS INTEGER)) AS period_number
    FROM orders o
    JOIN customer_first_month cfm ON o.customer_id = cfm.customer_id
    WHERE o.order_status = 'Completed'
),
cohort_matrix AS (
    SELECT
        cohort_month,
        period_number,
        COUNT(DISTINCT customer_id) AS active_users
    FROM cohort_orders
    GROUP BY cohort_month, period_number
),
cohort_sizes AS (
    SELECT
        cohort_month,
        active_users AS cohort_size
    FROM cohort_matrix
    WHERE period_number = 0
)
SELECT
    cm.cohort_month,
    cs.cohort_size,
    cm.period_number,
    cm.active_users,
    ROUND((CAST(cm.active_users AS REAL) / cs.cohort_size) * 100, 2) AS retention_pct
FROM cohort_matrix cm
JOIN cohort_sizes cs ON cm.cohort_month = cs.cohort_month
ORDER BY cm.cohort_month, cm.period_number;


-- ============================================================================
-- QUERY 6: Product & Category Margin Analysis
-- ============================================================================
SELECT
    p.category,
    p.product_id,
    p.product_name,
    p.list_price_inr,
    p.unit_cost_inr,
    SUM(oi.quantity) AS units_sold,
    ROUND(SUM(oi.quantity * oi.selling_unit_price_inr), 2) AS total_revenue_inr,
    ROUND(SUM(oi.line_gross_profit_inr), 2) AS total_gross_profit_inr,
    ROUND((SUM(oi.line_gross_profit_inr) / SUM(oi.quantity * oi.selling_unit_price_inr)) * 100, 2) AS realized_gross_margin_pct
FROM products p
JOIN order_items oi ON p.product_id = oi.product_id
JOIN orders o ON oi.order_id = o.order_id
WHERE o.order_status = 'Completed'
GROUP BY p.category, p.product_id, p.product_name, p.list_price_inr, p.unit_cost_inr
ORDER BY total_revenue_inr DESC;


-- ============================================================================
-- QUERY 7: Discount Depth Analysis (Full Price vs Promotional Elasticity)
-- ============================================================================
SELECT
    CASE
        WHEN o.discount_rate = 0.0 THEN '1. Full Price (0%)'
        WHEN o.discount_rate <= 0.10 THEN '2. Light Discount (1-10%)'
        WHEN o.discount_rate <= 0.20 THEN '3. Moderate Discount (11-20%)'
        ELSE '4. Deep Clearance (>20%)'
    END AS discount_tier,
    COUNT(DISTINCT o.order_id) AS order_count,
    ROUND(SUM(oi.quantity * oi.selling_unit_price_inr), 2) AS tier_revenue_inr,
    ROUND(SUM(oi.line_gross_profit_inr), 2) AS tier_gross_profit_inr,
    ROUND(AVG(oi.quantity * oi.selling_unit_price_inr), 2) AS avg_item_selling_price_inr,
    ROUND((SUM(oi.line_gross_profit_inr) / SUM(oi.quantity * oi.selling_unit_price_inr)) * 100, 2) AS realized_margin_pct
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.order_status = 'Completed'
GROUP BY discount_tier
ORDER BY discount_tier;


-- ============================================================================
-- QUERY 8: Inventory Stockout & Reorder Risk Watchlist
-- ============================================================================
SELECT
    p.product_id,
    p.product_name,
    p.category,
    i.on_hand_units,
    i.reorder_point_units,
    i.safety_stock_units,
    i.lead_time_days,
    CASE
        WHEN i.on_hand_units <= i.safety_stock_units THEN 'CRITICAL: Stockout Risk'
        WHEN i.on_hand_units <= i.reorder_point_units THEN 'WARNING: Reorder Required'
        ELSE 'OPTIMAL: Stock Healthy'
    END AS stock_status,
    i.reorder_point_units - i.on_hand_units AS recommended_reorder_qty
FROM inventory i
JOIN products p ON i.product_id = p.product_id
ORDER BY (i.on_hand_units - i.reorder_point_units) ASC;


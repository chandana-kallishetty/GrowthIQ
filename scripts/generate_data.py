"""
GrowthIQ Synthetic Data Generator
---------------------------------
Generates a realistic, statistically coherent synthetic dataset for a fashion and
athleisure D2C e-commerce brand operating in the Indian market.

Key characteristics:
- Reproducible via fixed random seed (default: 42).
- INR currency.
- Realistic Indian urban demographics and cities.
- Athleisure product catalogue with authentic list prices and unit costs.
- Multi-touch user journeys enabling First-Touch and Last-Touch attribution.
- E-commerce funnel events with monotonic timestamps.
- Robust cohort retention over 12 months (2025-01-01 to 2025-12-31).
- Distinct marketing campaigns across Meta Ads, Google Ads, Influencer, Email, Organic, and Direct.
- Explicitly documented as synthetic data for portfolio / analytical case-study purposes.
"""

import os
import random
from datetime import datetime, timedelta
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DATA_SYNTHETIC = DATA_DIR / "synthetic"
DATA_PROCESSED = DATA_DIR / "processed"
DATA_RAW = DATA_DIR / "raw"

RANDOM_SEED = 42
START_DATE = datetime(2025, 1, 1)
END_DATE = datetime(2025, 12, 31)
DAYS_IN_YEAR = (END_DATE - START_DATE).days + 1


def set_seed(seed=RANDOM_SEED):
    random.seed(seed)
    np.random.seed(seed)


def generate_products():
    """Generates product catalogue for athleisure & fashion D2C brand."""
    products_data = [
        # Leggings & Flared Pants
        ("P001", "Contour Seamless Leggings", "Leggings", "Women", 2499.0, 850.0, 0.66),
        ("P002", "High-Waist Sculpt Leggings", "Leggings", "Women", 2799.0, 920.0, 0.67),
        ("P003", "UltraLight Ankle Leggings", "Leggings", "Women", 2199.0, 720.0, 0.67),
        ("P004", "Studio Flared Pants", "Flared Pants", "Women", 2999.0, 1050.0, 0.65),
        ("P005", "Ribbed Flare Lounger", "Flared Pants", "Women", 2699.0, 910.0, 0.66),
        # Sports Bras
        ("P006", "CloudFlex Sports Bra", "Sports Bras", "Women", 1699.0, 520.0, 0.69),
        ("P007", "High-Impact Racerback Bra", "Sports Bras", "Women", 1999.0, 620.0, 0.69),
        ("P008", "Ribbed Longline Bra", "Sports Bras", "Women", 1799.0, 550.0, 0.69),
        # Shorts
        ("P009", "Everyday Biker Shorts", "Shorts", "Women", 1499.0, 480.0, 0.68),
        ("P010", "Core Training Shorts", "Shorts", "Men", 1799.0, 590.0, 0.67),
        ("P011", "Speed 2-in-1 Running Shorts", "Shorts", "Unisex", 2199.0, 750.0, 0.66),
        # Tops & Tanks
        ("P012", "Ribbed Crop Tank", "Tops & Tanks", "Women", 1299.0, 390.0, 0.70),
        ("P013", "Airy Performance Tee", "Tops & Tanks", "Men", 1599.0, 480.0, 0.70),
        ("P014", "Oversized Boyfriend Tee", "Tops & Tanks", "Women", 1499.0, 450.0, 0.70),
        # Jackets & Hoodies
        ("P015", "Sculpt Zip Jacket", "Jackets", "Women", 3799.0, 1350.0, 0.64),
        ("P016", "CloudKnit Zip Hoodie", "Jackets", "Unisex", 3999.0, 1420.0, 0.64),
        ("P017", "Luxe Windbreaker", "Jackets", "Unisex", 4499.0, 1600.0, 0.64),
        # Swimwear & Joggers
        ("P018", "Move Sculpt Swimsuit", "Swimwear", "Women", 3299.0, 1100.0, 0.67),
        ("P019", "Flex Tapered Joggers", "Joggers", "Unisex", 2899.0, 980.0, 0.66),
    ]

    df = pd.DataFrame(
        products_data,
        columns=[
            "product_id",
            "product_name",
            "category",
            "target_gender",
            "list_price_inr",
            "unit_cost_inr",
            "gross_margin_rate",
        ],
    )
    return df


def generate_categories(products_df):
    """Summarizes category hierarchy."""
    cat_df = (
        products_df.groupby("category")
        .agg(
            sku_count=("product_id", "count"),
            avg_price_inr=("list_price_inr", "mean"),
            avg_gross_margin=("gross_margin_rate", "mean"),
        )
        .reset_index()
    )
    cat_df["department"] = cat_df["category"].apply(
        lambda c: "Activewear" if c in ["Leggings", "Sports Bras", "Shorts"] else "Apparel & Outerwear"
    )
    return cat_df


def generate_customers(num_customers=2500):
    """Generates customer profiles across Indian tier-1 and tier-2 metro cities."""
    cities = [
        ("Mumbai", 0.22),
        ("Bengaluru", 0.20),
        ("Delhi NCR", 0.18),
        ("Hyderabad", 0.10),
        ("Pune", 0.08),
        ("Chennai", 0.07),
        ("Kolkata", 0.04),
        ("Ahmedabad", 0.04),
        ("Jaipur", 0.03),
        ("Chandigarh", 0.02),
        ("Kochi", 0.02),
    ]
    city_names, city_weights = zip(*cities)

    personas = [
        ("Fitness Enthusiast", 0.30),
        ("Casual Athleisure", 0.25),
        ("Pilates & Yoga Regular", 0.20),
        ("High-Intensity Athlete", 0.15),
        ("Trend-Conscious Shopper", 0.10),
    ]
    persona_names, persona_weights = zip(*personas)

    customers = []
    for i in range(1, num_customers + 1):
        cust_id = f"CUST{i:05d}"
        # Customer sign up date distributed over the year with slight acceleration in Q3/Q4
        day_offset = int(np.random.beta(a=1.4, b=1.2) * (DAYS_IN_YEAR - 1))
        signup_dt = START_DATE + timedelta(days=day_offset)
        city = np.random.choice(city_names, p=city_weights)
        persona = np.random.choice(persona_names, p=persona_weights)
        age = int(np.clip(np.random.normal(29, 6), 18, 55))

        customers.append(
            {
                "customer_id": cust_id,
                "signup_date": signup_dt.strftime("%Y-%m-%d"),
                "city": city,
                "age": age,
                "persona_seed": persona,
            }
        )

    return pd.DataFrame(customers)


def generate_marketing_channels_and_campaigns():
    """Defines campaign metadata with channel mappings and targeting objectives."""
    campaigns = [
        # Meta Ads (Paid Social)
        ("Paid Social", "Meta_Spring_Sculpt", "Prospecting", 0.024, 22.0, 480.0),
        ("Paid Social", "Meta_Summer_Active_Drop", "Prospecting", 0.028, 26.0, 520.0),
        ("Paid Social", "Meta_Festive_Sale_Promo", "Promotional", 0.035, 30.0, 600.0),
        ("Paid Social", "Meta_Retargeting_Catalog", "Retargeting", 0.042, 18.0, 420.0),
        ("Paid Social", "Meta_Evergreen_Leggings", "Prospecting", 0.022, 20.0, 450.0),
        # Google Ads (Paid Search)
        ("Paid Search", "GAds_Brand_Exact", "Brand", 0.065, 14.0, 320.0),
        ("Paid Search", "GAds_Category_Athleisure", "Generic", 0.032, 28.0, 490.0),
        ("Paid Search", "GAds_PMax_Shopping", "Shopping", 0.040, 24.0, 460.0),
        ("Paid Search", "GAds_Competitor_Conquest", "Conquesting", 0.018, 38.0, 580.0),
        # Influencer Marketing
        ("Influencer", "Inf_Yoga_Creators_Collab", "Influencer", 0.031, 35.0, 650.0),
        ("Influencer", "Inf_Fitness_Ambassador_Q2", "Influencer", 0.028, 32.0, 620.0),
        ("Influencer", "Inf_Festive_Gifting_Unbox", "Influencer", 0.036, 40.0, 710.0),
        # Email Marketing
        ("Email", "Email_Welcome_Flow_10Off", "Lifecycle", 0.085, 3.5, 45.0),
        ("Email", "Email_Cart_Recovery_Series", "Abandoned Cart", 0.110, 4.0, 50.0),
        ("Email", "Email_VIP_Early_Access", "Retention", 0.095, 3.0, 40.0),
        ("Email", "Email_Winback_Inactive_90D", "Winback", 0.045, 2.5, 35.0),
        # Organic Search & Direct (Non-paid / nominal cost)
        ("Organic Search", "Organic_SEO_Content", "SEO", 0.030, 0.0, 0.0),
        ("Direct", "Direct_Brand_Traffic", "Direct", 0.038, 0.0, 0.0),
    ]

    df = pd.DataFrame(
        campaigns,
        columns=["channel", "campaign", "campaign_type", "expected_cvr", "target_cpc", "target_cpm"],
    )
    return df


def generate_campaign_spend(campaigns_df):
    """
    Generates daily campaign expenditure, impressions, and clicks for 2025.
    Paid channels have realistic daily budgets with seasonality peaks around Oct-Dec.
    """
    daily_records = []
    paid_campaigns = campaigns_df[campaigns_df["target_cpc"] > 0]

    for day in range(DAYS_IN_YEAR):
        curr_date = START_DATE + timedelta(days=day)
        month = curr_date.month
        # Q4 festive lift multiplier in India (Diwali / wedding season / winter fitness)
        season_multiplier = 1.0 + (0.45 if month in [10, 11] else (0.25 if month == 12 else (0.1 if month == 1 else 0.0)))
        weekend_multiplier = 1.15 if curr_date.weekday() in [5, 6] else 1.0

        for _, camp in paid_campaigns.iterrows():
            # Base daily budget in INR
            if "Brand_Exact" in camp["campaign"]:
                base_budget = 900.0
            elif "Meta_Retargeting" in camp["campaign"]:
                base_budget = 1200.0
            elif "Email" in camp["channel"]:
                base_budget = 120.0  # nominal tool / ESP delivery cost
            elif "Festive" in camp["campaign"]:
                base_budget = 2400.0 if month in [10, 11] else 800.0
            elif "PMax" in camp["campaign"]:
                base_budget = 1800.0
            elif "Influencer" in camp["channel"]:
                base_budget = 1500.0
            else:
                base_budget = 1100.0

            daily_spend = base_budget * season_multiplier * weekend_multiplier * np.random.uniform(0.85, 1.18)
            cpc = camp["target_cpc"] * np.random.uniform(0.9, 1.15)
            cpm = camp["target_cpm"] * np.random.uniform(0.92, 1.12)

            clicks = int(max(1, daily_spend / max(0.5, cpc)))
            impressions = int(max(clicks * 15, (daily_spend / max(1.0, cpm)) * 1000))

            daily_records.append(
                {
                    "spend_date": curr_date.strftime("%Y-%m-%d"),
                    "channel": camp["channel"],
                    "campaign": camp["campaign"],
                    "spend_inr": round(float(daily_spend), 2),
                    "impressions": impressions,
                    "clicks": clicks,
                }
            )

    return pd.DataFrame(daily_records)


def generate_sessions_and_orders(customers_df, products_df, campaigns_df):
    """
    Generates realistic user sessions, event funnels, orders, and order items.
    Ensures referential integrity across sessions, events, orders, customers, and products.
    """
    devices = [("Mobile", 0.74), ("Desktop", 0.22), ("Tablet", 0.04)]
    dev_names, dev_weights = zip(*devices)

    channel_weights = [
        ("Paid Social", 0.32),
        ("Paid Search", 0.24),
        ("Organic Search", 0.18),
        ("Direct", 0.12),
        ("Email", 0.08),
        ("Influencer", 0.06),
    ]
    ch_names, ch_weights = zip(*channel_weights)

    # Pre-select customers who make purchases
    num_customers = len(customers_df)
    customer_ids = customers_df["customer_id"].tolist()
    customer_signup = dict(zip(customers_df["customer_id"], pd.to_datetime(customers_df["signup_date"])))

    # ~55% of registered customers place at least 1 order; of those, ~30% place 2+ orders
    ordered_customers = random.sample(customer_ids, k=int(num_customers * 0.56))
    repeat_customers = set(random.sample(ordered_customers, k=int(len(ordered_customers) * 0.32)))
    vip_repeat_customers = set(random.sample(list(repeat_customers), k=int(len(repeat_customers) * 0.25)))

    sessions = []
    events = []
    orders = []
    order_items = []

    session_counter = 1
    event_counter = 1
    order_counter = 1

    # Campaign lookup by channel
    channel_campaign_map = {}
    for ch in campaigns_df["channel"].unique():
        channel_campaign_map[ch] = campaigns_df[campaigns_df["channel"] == ch]["campaign"].tolist()

    # Track customer touches for attribution (first touch vs last touch)
    customer_first_touch = {}

    # 1. Generate Order Journeys for Purchasing Customers
    for cust_id in ordered_customers:
        signup_dt = customer_signup[cust_id]
        if cust_id in vip_repeat_customers:
            order_counts = random.choice([3, 4, 5, 6])
        elif cust_id in repeat_customers:
            order_counts = random.choice([2, 3])
        else:
            order_counts = 1

        last_order_dt = signup_dt
        for order_idx in range(order_counts):
            if order_idx == 0:
                # First order shortly after signup (1-14 days)
                order_dt = signup_dt + timedelta(days=random.randint(0, 12), hours=random.randint(1, 23))
                # First order channel mix leans towards Paid Social / Search / Influencer
                chosen_channel = np.random.choice(
                    ch_names, p=[0.38, 0.28, 0.14, 0.08, 0.04, 0.08]
                )
            else:
                # Subsequent orders spaced 20 to 90 days later
                days_gap = random.randint(22, 95)
                order_dt = last_order_dt + timedelta(days=days_gap, hours=random.randint(1, 23))
                # Repeat orders lean heavily towards Email, Direct, Organic Search
                chosen_channel = np.random.choice(
                    ch_names, p=[0.12, 0.10, 0.22, 0.26, 0.25, 0.05]
                )

            if order_dt > END_DATE:
                break
            last_order_dt = order_dt

            chosen_campaign = random.choice(channel_campaign_map[chosen_channel])
            chosen_device = np.random.choice(dev_names, p=dev_weights)

            # Record customer touchpoints
            if cust_id not in customer_first_touch:
                customer_first_touch[cust_id] = {
                    "first_channel": chosen_channel,
                    "first_campaign": chosen_campaign,
                    "first_touch_date": order_dt.strftime("%Y-%m-%d"),
                }

            # Create Converting Session
            sess_id = f"SESS{session_counter:07d}"
            session_counter += 1

            # Realistic simulated cost proxy per session
            if chosen_channel == "Paid Social":
                sess_cost = round(random.uniform(22.0, 34.0), 2)
            elif chosen_channel == "Paid Search":
                sess_cost = round(random.uniform(16.0, 32.0), 2)
            elif chosen_channel == "Influencer":
                sess_cost = round(random.uniform(25.0, 45.0), 2)
            elif chosen_channel == "Email":
                sess_cost = round(random.uniform(1.5, 3.5), 2)
            else:
                sess_cost = 0.0

            sessions.append(
                {
                    "session_id": sess_id,
                    "session_date": order_dt.strftime("%Y-%m-%d"),
                    "customer_id": cust_id,
                    "channel": chosen_channel,
                    "campaign": chosen_campaign,
                    "device": chosen_device,
                    "landing_page": random.choice(
                        ["/collections/leggings", "/products/cloudflex-bra", "/home", "/collections/new-arrivals"]
                    ),
                    "session_cost_inr": sess_cost,
                }
            )

            # Monotonic event sequence leading to purchase
            curr_ts = order_dt
            events.append(
                {
                    "event_id": f"EVT{event_counter:08d}",
                    "session_id": sess_id,
                    "event_timestamp": curr_ts.strftime("%Y-%m-%d %H:%M:%S"),
                    "event_name": "session_start",
                }
            )
            event_counter += 1

            curr_ts += timedelta(seconds=random.randint(20, 90))
            events.append(
                {
                    "event_id": f"EVT{event_counter:08d}",
                    "session_id": sess_id,
                    "event_timestamp": curr_ts.strftime("%Y-%m-%d %H:%M:%S"),
                    "event_name": "view_item",
                }
            )
            event_counter += 1

            curr_ts += timedelta(seconds=random.randint(30, 180))
            events.append(
                {
                    "event_id": f"EVT{event_counter:08d}",
                    "session_id": sess_id,
                    "event_timestamp": curr_ts.strftime("%Y-%m-%d %H:%M:%S"),
                    "event_name": "add_to_cart",
                }
            )
            event_counter += 1

            curr_ts += timedelta(seconds=random.randint(40, 240))
            events.append(
                {
                    "event_id": f"EVT{event_counter:08d}",
                    "session_id": sess_id,
                    "event_timestamp": curr_ts.strftime("%Y-%m-%d %H:%M:%S"),
                    "event_name": "begin_checkout",
                }
            )
            event_counter += 1

            curr_ts += timedelta(seconds=random.randint(30, 180))
            events.append(
                {
                    "event_id": f"EVT{event_counter:08d}",
                    "session_id": sess_id,
                    "event_timestamp": curr_ts.strftime("%Y-%m-%d %H:%M:%S"),
                    "event_name": "purchase",
                }
            )
            event_counter += 1

            # Order creation
            order_id = f"ORD{order_counter:06d}"
            order_counter += 1

            # Order status (Completed ~93%, Refunded ~5%, Cancelled ~2%)
            status_roll = random.random()
            if status_roll < 0.93:
                order_status = "Completed"
            elif status_roll < 0.98:
                order_status = "Refunded"
            else:
                order_status = "Cancelled"

            # Discount rate: Full price (45%), 10% off (22%), 15% off (15%), 20% off (12%), 30% off (6%)
            disc_roll = random.random()
            if disc_roll < 0.45:
                disc_rate = 0.0
            elif disc_roll < 0.67:
                disc_rate = 0.10
            elif disc_roll < 0.82:
                disc_rate = 0.15
            elif disc_roll < 0.94:
                disc_rate = 0.20
            else:
                disc_rate = 0.30

            orders.append(
                {
                    "order_id": order_id,
                    "customer_id": cust_id,
                    "session_id": sess_id,
                    "order_date": order_dt.strftime("%Y-%m-%d"),
                    "channel": chosen_channel,
                    "campaign": chosen_campaign,
                    "device": chosen_device,
                    "discount_rate": disc_rate,
                    "order_status": order_status,
                }
            )

            # Order items (1 to 4 distinct items per order)
            num_items = random.choices([1, 2, 3, 4], weights=[0.58, 0.28, 0.10, 0.04])[0]
            sampled_products = products_df.sample(n=num_items, replace=False)

            for _, prod in sampled_products.iterrows():
                qty = random.choices([1, 2], weights=[0.88, 0.12])[0]
                list_price = prod["list_price_inr"]
                unit_cost = prod["unit_cost_inr"]
                selling_price = round(list_price * (1.0 - disc_rate), 2)
                line_profit = round((selling_price - unit_cost) * qty, 2)

                order_items.append(
                    {
                        "order_id": order_id,
                        "product_id": prod["product_id"],
                        "quantity": qty,
                        "list_unit_price_inr": list_price,
                        "selling_unit_price_inr": selling_price,
                        "line_gross_profit_inr": line_profit,
                    }
                )

    # 2. Generate Non-converting Browsing Sessions across 2025 to reflect realistic funnel drop-off
    total_target_sessions = 42000
    non_converting_count = total_target_sessions - len(sessions)

    for _ in range(non_converting_count):
        day_offset = random.randint(0, DAYS_IN_YEAR - 1)
        sess_dt = START_DATE + timedelta(days=day_offset, hours=random.randint(0, 23), minutes=random.randint(0, 59))
        chosen_channel = np.random.choice(ch_names, p=ch_weights)
        chosen_campaign = random.choice(channel_campaign_map[chosen_channel])
        chosen_device = np.random.choice(dev_names, p=dev_weights)

        # 40% known registered customer browsing, 60% anonymous / prospective visitor
        if random.random() < 0.40:
            c_id = random.choice(customer_ids)
        else:
            c_id = None

        if chosen_channel == "Paid Social":
            sess_cost = round(random.uniform(18.0, 30.0), 2)
        elif chosen_channel == "Paid Search":
            sess_cost = round(random.uniform(14.0, 28.0), 2)
        elif chosen_channel == "Influencer":
            sess_cost = round(random.uniform(22.0, 38.0), 2)
        elif chosen_channel == "Email":
            sess_cost = round(random.uniform(1.2, 3.0), 2)
        else:
            sess_cost = 0.0

        sess_id = f"SESS{session_counter:07d}"
        session_counter += 1

        sessions.append(
            {
                "session_id": sess_id,
                "session_date": sess_dt.strftime("%Y-%m-%d"),
                "customer_id": c_id,
                "channel": chosen_channel,
                "campaign": chosen_campaign,
                "device": chosen_device,
                "landing_page": random.choice(
                    ["/home", "/collections/leggings", "/collections/sale", "/collections/new-arrivals", "/products/studio-flare"]
                ),
                "session_cost_inr": sess_cost,
            }
        )

        # Funnel stage dropoff for non-converting sessions
        # 100% session_start
        curr_ts = sess_dt
        events.append(
            {
                "event_id": f"EVT{event_counter:08d}",
                "session_id": sess_id,
                "event_timestamp": curr_ts.strftime("%Y-%m-%d %H:%M:%S"),
                "event_name": "session_start",
            }
        )
        event_counter += 1

        funnel_depth = random.random()
        if funnel_depth < 0.58:  # 58% view an item
            curr_ts += timedelta(seconds=random.randint(15, 75))
            events.append(
                {
                    "event_id": f"EVT{event_counter:08d}",
                    "session_id": sess_id,
                    "event_timestamp": curr_ts.strftime("%Y-%m-%d %H:%M:%S"),
                    "event_name": "view_item",
                }
            )
            event_counter += 1

            if funnel_depth < 0.20:  # 20% add to cart
                curr_ts += timedelta(seconds=random.randint(30, 120))
                events.append(
                    {
                        "event_id": f"EVT{event_counter:08d}",
                        "session_id": sess_id,
                        "event_timestamp": curr_ts.strftime("%Y-%m-%d %H:%M:%S"),
                        "event_name": "add_to_cart",
                    }
                )
                event_counter += 1

                if funnel_depth < 0.07:  # 7% begin checkout and abandon
                    curr_ts += timedelta(seconds=random.randint(40, 180))
                    events.append(
                        {
                            "event_id": f"EVT{event_counter:08d}",
                            "session_id": sess_id,
                            "event_timestamp": curr_ts.strftime("%Y-%m-%d %H:%M:%S"),
                            "event_name": "begin_checkout",
                        }
                    )
                    event_counter += 1

    sessions_df = pd.DataFrame(sessions).sort_values("session_date").reset_index(drop=True)
    events_df = pd.DataFrame(events).sort_values("event_timestamp").reset_index(drop=True)
    orders_df = pd.DataFrame(orders).sort_values("order_date").reset_index(drop=True)
    order_items_df = pd.DataFrame(order_items).reset_index(drop=True)

    return sessions_df, events_df, orders_df, order_items_df, customer_first_touch


def generate_inventory(products_df):
    """Generates inventory snapshots including stock levels, reorder points, and lead times."""
    inventory_records = []
    snapshot_date = "2025-12-31"

    for _, prod in products_df.iterrows():
        # High-demand items like Contour Leggings & CloudFlex Bra have active reorders
        p_id = prod["product_id"]
        if p_id in ["P001", "P006"]:
            on_hand = random.randint(18, 45)
            reorder_pt = 50
            safety_stock = 25
        elif p_id in ["P002", "P004", "P012"]:
            on_hand = random.randint(40, 95)
            reorder_pt = 60
            safety_stock = 30
        else:
            on_hand = random.randint(70, 220)
            reorder_pt = 40
            safety_stock = 20

        lead_days = random.choice([7, 10, 14, 21])

        inventory_records.append(
            {
                "product_id": p_id,
                "on_hand_units": on_hand,
                "reorder_point_units": reorder_pt,
                "safety_stock_units": safety_stock,
                "lead_time_days": lead_days,
                "snapshot_date": snapshot_date,
            }
        )

    return pd.DataFrame(inventory_records)


def main():
    print("=" * 60)
    print("GrowthIQ Synthetic Data Generation")
    print("=" * 60)
    set_seed(RANDOM_SEED)

    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(DATA_SYNTHETIC, exist_ok=True)
    os.makedirs(DATA_PROCESSED, exist_ok=True)
    os.makedirs(DATA_RAW, exist_ok=True)

    print("1. Generating products and categories...")
    products_df = generate_products()
    categories_df = generate_categories(products_df)

    print("2. Generating customer demographic profiles...")
    customers_df = generate_customers(num_customers=2500)

    print("3. Generating marketing channels and campaign structures...")
    campaigns_df = generate_marketing_channels_and_campaigns()

    print("4. Generating campaign daily expenditure, impressions, and clicks...")
    spend_df = generate_campaign_spend(campaigns_df)

    print("5. Generating user sessions, funnels, orders, and order items...")
    sessions_df, events_df, orders_df, order_items_df, customer_first_touch = (
        generate_sessions_and_orders(customers_df, products_df, campaigns_df)
    )

    print("6. Generating inventory snapshot...")
    inventory_df = generate_inventory(products_df)

    # Save to data/ and data/synthetic/
    datasets = {
        "products.csv": products_df,
        "product_categories.csv": categories_df,
        "customers.csv": customers_df,
        "campaigns.csv": campaigns_df,
        "campaign_spend.csv": spend_df,
        "sessions.csv": sessions_df,
        "events.csv": events_df,
        "orders.csv": orders_df,
        "order_items.csv": order_items_df,
        "inventory.csv": inventory_df,
    }

    print("\nWriting generated datasets...")
    for filename, df in datasets.items():
        # Save to primary data/
        primary_path = DATA_DIR / filename
        df.to_csv(primary_path, index=False)
        # Save to synthetic/
        synth_path = DATA_SYNTHETIC / filename
        df.to_csv(synth_path, index=False)
        print(f"  ✓ {filename:<24} {len(df):>7,} rows")

    # Summary Statistics
    items_rev = order_items_df["selling_unit_price_inr"] * order_items_df["quantity"]
    total_rev = items_rev.sum()
    total_spend = spend_df["spend_inr"].sum()
    total_orders = len(orders_df)
    purchasers = orders_df["customer_id"].nunique()
    repeat_purchasers = (orders_df.groupby("customer_id").size() > 1).sum()

    print("\n" + "=" * 60)
    print("DATASET VALIDATION SUMMARY:")
    print(f"  Total Sessions:           {len(sessions_df):,}")
    print(f"  Total Events:             {len(events_df):,}")
    print(f"  Total Orders:             {total_orders:,}")
    print(f"  Total Order Items:        {len(order_items_df):,}")
    print(f"  Unique Purchasing Custs:  {purchasers:,}")
    print(f"  Repeat Purchasers:        {repeat_purchasers:,} ({repeat_purchasers/purchasers:.1%})")
    print(f"  Total Revenue (INR):      ₹{total_rev:,.2f}")
    print(f"  Average Order Value (AOV):₹{total_rev/total_orders:,.2f}")
    print(f"  Total Marketing Spend:    ₹{total_spend:,.2f}")
    print(f"  Blended ROAS:             {total_rev/total_spend:.2f}x")
    print(f"  Blended CAC:              ₹{total_spend/purchasers:,.2f}")
    print("=" * 60)


if __name__ == "__main__":
    main()


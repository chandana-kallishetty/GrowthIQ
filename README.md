# GrowthIQ — End-to-End E-Commerce Marketing Intelligence Platform

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.40%2B-FF4B4B.svg)](https://streamlit.io/)
[![Plotly](https://img.shields.io/badge/Plotly-5.20%2B-3F4F75.svg)](https://plotly.com/)
[![SQLite](https://img.shields.io/badge/SQLite-3-003B57.svg)](https://www.sqlite.org/)
[![Pytest](https://img.shields.io/badge/Tests-20%20Passed-brightgreen.svg)](https://docs.pytest.org/)
[![License](https://img.shields.io/badge/Data-100%25%20Synthetic-orange.svg)](#data-governance--synthetic-disclaimer)

> **Strategic Portfolio Project:** An end-to-end e-commerce marketing intelligence platform designed for fashion and athleisure D2C commerce, inspired by modern athleisure retail operations. Built to demonstrate the comprehensive analytical, data engineering, statistical modeling, and UI/UX capabilities required of a **Senior Marketing Data Analyst / Analytics Engineer**.

---

## 🏛️ Executive Summary

GrowthIQ bridges the gap between raw e-commerce telemetry and high-conviction commercial decisions. Operating on a calendar year 2025 dataset (42,000 browsing sessions, 83,600 telemetry events, 1,988 completed orders, and ₹8.21M in realized sales), the platform transforms fragmented touchpoints into decision-ready strategic intelligence.

### Key Business Questions Answered:
1. **Acquisition Efficiency:** Which marketing channels and advertising campaigns generate the highest ROAS and lowest CAC?
2. **Attribution Specialization:** How does channel return shift between First-Touch (discovery origin) and Last-Touch (conversion closing) attribution?
3. **Merchandise Demand:** Which fashion categories and hero SKUs drive volume, and which maintain the highest realized gross margins?
4. **Customer Retention:** What proportion of buyers place repeat orders, and how does retention evolve across monthly acquisition cohorts?
5. **Customer Segmentation:** Which behavioral segments (VIP Champions, Loyalists, At-Risk High Value) represent the highest revenue exposure and lifetime value?
6. **Funnel Friction:** Where do customers abandon the shopping journey (browse, item view, cart add, checkout), and what is the device disparity?
7. **Promotional Discipline:** How severely do clearance discount bands (>20%) erode gross margins compared to full-price orders?
8. **Supply Chain Health:** Which SKUs have breached safety stock thresholds and face imminent stockout risks?

---

## 🛠️ Technology Stack

| Layer | Technologies | Rationale |
|---|---|---|
| **Core Analytics & Math** | `Python 3.10+`, `Pandas`, `NumPy`, `Scikit-Learn` | High-performance matrix arithmetic, quantile scoring, feature standardisation, and unsupervised K-Means clustering. |
| **Relational Database** | `SQLite 3`, `SQL` | DDL schema with primary key constraints, foreign key enforcement (`PRAGMA foreign_keys = ON;`), WAL mode, and analytical CTEs. |
| **Interactive UI & SaaS Design** | `Streamlit`, `Plotly`, `Custom CSS` | Responsive multi-page SaaS dashboard adhering to a bespoke luxury visual identity (Warm ivory `#FFFDF9`, Deep burgundy `#4B2634`, Champagne-gold `#C5A059`). |
| **Data Quality & Testing** | `Pytest` | Automated unit tests covering referential integrity, primary key uniqueness, KPI calculations, and database parity. |
| **Version Control & CI/CD** | `Git`, `GitHub` | Clean, modular project structure with strict separation of concerns. |

---

## 📁 Repository Map

```text
GrowthIQ/
├── app.py                             # Central Strategic Launchpad & Executive Directory
├── requirements.txt                   # Production dependencies
├── pytest.ini                         # Pytest configuration
├── README.md                          # Comprehensive project documentation
├── REFERENCES.md                      # Official documentation citations & methodologies
├── .gitignore                         # Version control exclusions
│
├── pages/                             # Multi-Page Streamlit Analytical Modules
│   ├── 01_Executive_Overview.py       # Top-line revenue, unit economics, category mix
│   ├── 02_Marketing_Performance.py    # Channel attribution, campaign ROAS/CAC, CTR/CPC
│   ├── 03_Customer_Intelligence.py    # RFM segmentation, K-Means clustering personas
│   ├── 04_Product_Analytics.py        # Hero SKUs, gross margins, discount tiers, stockout alerts
│   ├── 05_Conversion_Funnel.py        # 5-stage milestone funnel, stage leakage, device friction
│   ├── 06_Cohort_Analysis.py          # Monthly retention triangle heatmap, repeat velocity
│   └── 07_Data_Quality.py             # Automated audits: PK uniqueness, FK integrity, table profiles
│
├── src/                               # Modular Backend Source Code
│   ├── data/                          # Data Ingestion, Cleaning & Quality Assurance
│   │   ├── loader.py                  # CSV ingestion and SQLite bulk population
│   │   ├── cleaning.py                # Line-level calculation and timestamp normalization
│   │   └── validation.py              # Automated data-quality & referential integrity audits
│   │
│   ├── analytics/                     # Analytical Calculation Engine
│   │   ├── kpis.py                    # Revenue, AOV, gross margin, spend, ROAS, CAC, MoM growth
│   │   ├── attribution.py             # First-Touch vs. Last-Touch multi-touch attribution
│   │   ├── segmentation.py            # RFM scoring (1-4) & unsupervised K-Means clustering
│   │   ├── cohorts.py                 # Monthly cohort retention matrices & customer tenure
│   │   ├── funnel.py                  # Step-by-step funnel drop-offs and device comparisons
│   │   └── products.py                # SKU demand, category economics, discount bands, inventory
│   │
│   ├── database/                      # SQLite Relational Manager
│   │   ├── connection.py              # Thread-safe connection pool with foreign keys & WAL mode
│   │   └── queries.py                 # SQL execution and analytical queries parser
│   │
│   └── visualisation/                 # Visual Design & Streamlit Components
│       ├── charts.py                  # Plotly custom styling (Ivory, Burgundy, Gold, Taupe)
│       └── ui.py                      # Reusable SaaS cards, sidebar filters, insights callouts
│
├── sql/                               # Relational Schema & Analysis Queries
│   ├── schema.sql                     # Normalized SQLite DDL with CHECK constraints & indexes
│   └── analysis_queries.sql           # Production SQL analytical queries (CTEs, window functions)
│
├── data/                              # Interconnected Relational Datasets (Synthetic)
│   ├── customers.csv                  # 2,500 customer profiles across Indian metros
│   ├── products.csv                   # 19 athleisure SKUs with unit costs & list prices
│   ├── product_categories.csv         # 8 merchandise categories and department groupings
│   ├── campaigns.csv                  # 18 marketing campaigns across paid & lifecycle channels
│   ├── campaign_spend.csv             # 5,840 daily campaign spend, impression, and click records
│   ├── sessions.csv                   # 42,000 web sessions with traffic source & cost proxy
│   ├── events.csv                     # 83,644 granular GA4-style funnel milestone events
│   ├── orders.csv                     # 1,988 customer orders with discount rates & statuses
│   ├── order_items.csv                # 3,190 line items with selling prices & line gross profits
│   ├── inventory.csv                  # Warehouse stock snapshot with safety thresholds & lead times
│   └── synthetic/                     # Direct mirrors of generated synthetic datasets
│
├── scripts/                           # Reproducible CLI Utilities
│   ├── generate_data.py               # Seeded synthetic e-commerce data generation engine
│   └── build_database.py              # SQLite relational schema builder & database populator
│
├── tests/                             # Automated Test Suite (20 Tests, 100% Passing)
│   ├── test_data_quality.py           # Primary keys, foreign keys, non-negative values, event taxonomies
│   ├── test_analytics.py              # KPI math, AOV, ROAS, CAC, conversion rate, empty-safe handling
│   ├── test_calculations.py           # RFM scoring, K-Means clustering, attribution, cohort retention
│   └── test_database.py               # SQLite connectivity, table validation, SQL-Pandas KPI parity
│
├── docs/                              # Comprehensive Documentation
│   ├── PROJECT_BRIEF.md               # Stakeholder challenge, objectives, and deliverables
│   ├── DATA_DICTIONARY.md             # Schema specification for all 10 tables
│   ├── METRIC_DICTIONARY.md           # Mathematical formulas, grains, and business caveats
│   ├── METHODOLOGY.md                 # RFM, K-Means, attribution, cohort, and funnel methodologies
│   ├── BUSINESS_INSIGHTS.md           # Strategic commercial recommendations and findings
│   └── USER_GUIDE.md                  # Step-by-step user guide for dashboard and CLI tools
│
└── assets/                            # Brand Assets & Vector Art
    └── logo.svg                       # GrowthIQ geometric emblem and typography vector logo
```

---

## ⚡ Quick Start (Local Setup)

### 1. Clone or Extract the Repository
```bash
git clone https://github.com/your-username/GrowthIQ.git
cd GrowthIQ
```

### 2. Activate Virtual Environment
```powershell
# Windows PowerShell
.\.venv\Scripts\Activate.ps1

# Windows Command Prompt
.venv\Scripts\activate.bat

# macOS / Linux
source .venv/bin/activate
```

*(If creating a fresh virtual environment: `python -m venv .venv` followed by `pip install -r requirements.txt`)*

### 3. Launch the Streamlit Platform
```bash
streamlit run app.py
```
Open the local browser URL (normally `http://localhost:8501`).

---

## 🧪 Automated Testing & Data Quality Verification

The platform includes an automated testing suite built with `pytest` covering 20 comprehensive unit and integration tests.

### Running the Test Suite
```bash
.\.venv\Scripts\python.exe -m pytest tests -v
```

### Test Coverage Summary:
- **`test_data_quality.py` (6 tests):** Verifies primary key uniqueness across all 10 tables, foreign key referential integrity (zero orphaned orders, order items, sessions, or events), non-negative quantities and selling prices, valid discount ranges (0.0–1.0), and standard GA4 event taxonomies.
- **`test_analytics.py` (4 tests):** Validates line-level order facts aggregation, executive KPI calculations (AOV, ROAS, CAC, Gross Margin), unique session deduplication in funnels, and division-by-zero resilience on empty DataFrames.
- **`test_calculations.py` (6 tests):** Validates quantile-based RFM scoring, K-Means clustering execution and persona labeling, First-Touch vs Last-Touch revenue conservation, cohort retention matrix properties ($M_0 = 100\%$, $M_t \le 100\%$), and discount band gross margin degradation.
- **`test_database.py` (4 tests):** Tests active SQLite connection, foreign key enforcement pragma, table existence, execution of all 8 analytical SQL queries in `sql/analysis_queries.sql`, and exact mathematical parity between SQL query results and Python calculations.

```text
============================== test session starts ==============================
platform win32 -- Python 3.14.10, pytest-8.4.2
collected 20 items

tests/test_analytics.py ....                                              [ 20%]
tests/test_calculations.py ......                                         [ 50%]
tests/test_data_quality.py ......                                         [ 80%]
tests/test_database.py ....                                               [100%]

============================== 20 passed in 2.62s ===============================
```

---

## 📊 Analytical Capabilities & Features

### 1. Multi-Touch Attribution Engine
- **First-Touch Attribution (FT):** Credits revenue to the customer's earliest recorded discovery touchpoint.
- **Last-Touch Attribution (LT):** Credits revenue directly to the converting order session.
- **Channel Role Specialization:** Mathematically quantifies channel roles ($\Delta = \text{Revenue}_{\text{LT}} - \text{Revenue}_{\text{FT}}$), identifying **Paid Social** as the primary top-of-funnel customer introducer (-₹830k variance) and **Email** as the primary conversion closer (+₹420k variance).

### 2. Behavioral RFM Customer Segmentation & K-Means Clustering
- **RFM Quantile Scoring:** Assigns 1–4 scores across Recency, Frequency, and Monetary Value, classifying customers into actionable tiers: *VIP Champions*, *Loyal Customers*, *Promising Newcomers*, *Potential Loyalists*, *At-Risk High Value*, *Hibernating / Lapsed*, and *Active Regulars*.
- **Unsupervised Machine Learning:** Applies standard-scaled K-Means clustering ($k=4$) on log-transformed transaction metrics to surface distinct customer personas (*High-Value Frequent*, *Dormant / Churned*, *Recent Single-Order*, *Nurturable Active*).

### 3. Triangular Monthly Cohort Retention
- Groups buyers by first-order calendar month and tracks active purchasing retention across subsequent tenure intervals ($M_0$ through $M_{11}$).
- Provides interactive retention rate heatmaps, active customer count matrices, and cumulative cohort revenue curves.

### 4. 5-Stage E-Commerce Funnel & Device Friction
- Analyzes visitor progression through standard milestones: `session_start` $\to$ `view_item` $\to$ `add_to_cart` $\to$ `begin_checkout` $\to$ `purchase`.
- Identifies the primary drop-off bottleneck (add-to-cart leakage at 62.5%) and quantifies device conversion disparities (Desktop 4.12% vs Mobile 2.85%).

### 5. Merchandise Economics & Supply Chain Risk
- Ranks SKUs by realized net revenue, units sold, and realized gross margins.
- Evaluates promotional discount depth across discrete bands, proving that clearance discounts (>20%) erode margins from 67.4% down to 52.6%.
- Dynamic inventory watchlist flags SKUs as `CRITICAL`, `REORDER`, or `HEALTHY` based on safety stock thresholds and replenishment lead times.

---

## 🔒 Data Governance & Synthetic Disclaimer

**Important Portfolio Notice:**
All customer profiles, contact details, transaction histories, advertising expenditures, and inventory stock balances contained in GrowthIQ are **100% synthetically generated** using reproducible algorithmic models (`scripts/generate_data.py`).
- Primary currency: **Indian Rupee (INR - ₹)**.
- The project is an independent case study inspired by the publicly observable product categories and e-commerce customer experience of modern athleisure brands.
- GrowthIQ does not access, store, or claim access to any proprietary corporate databases, private Shopify stores, GA4 properties, or advertising accounts.

---

## 📄 Documentation Index

- [Project Brief](docs/PROJECT_BRIEF.md): Stakeholder objectives, business challenge, and success criteria.
- [Data Dictionary](docs/DATA_DICTIONARY.md): Granular schemas, primary keys, and column definitions for all 10 tables.
- [Metric Dictionary](docs/METRIC_DICTIONARY.md): Mathematical formulas, operational grains, and analytical caveats.
- [Analytical Methodology](docs/METHODOLOGY.md): Technical deep-dive into RFM scoring, K-Means clustering, attribution, and cohort math.
- [Strategic Business Insights](docs/BUSINESS_INSIGHTS.md): Executive summary of empirical findings and growth opportunities.
- [Platform User Guide](docs/USER_GUIDE.md): Step-by-step navigation instructions and CLI operations.
- [Technical References](REFERENCES.md): Official technical documentation and academic citations.

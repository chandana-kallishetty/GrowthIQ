# GrowthIQ — Strategic Project Brief

## 1. Executive Summary & Identity
- **Project Name:** GrowthIQ
- **Full Title:** GrowthIQ – E-Commerce Marketing Intelligence Platform
- **Domain:** Fashion, athleisure, and apparel Direct-to-Consumer (D2C) e-commerce.
- **Business Context:** An independent analytical case study inspired by the publicly observable e-commerce customer experience and product categories of modern athleisure brands.
- **Currency:** Indian Rupee (INR - ₹).
- **Temporal Scope:** Full calendar year 2025 (2025-01-01 to 2025-12-31).

---

## 2. Business Challenge & Objectives
Modern D2C e-commerce brands face severe measurement headwinds: rising customer acquisition costs (CAC) across paid social platforms, post-iOS14 signal degradation, customer churn, and margin erosion from indiscriminate promotional discounting.

GrowthIQ was conceived to unify disparate e-commerce telemetry—website sessions, event funnels, media expenditures, product transactions, and warehouse stock balances—into a centralized, reproducible marketing intelligence platform.

### Core Strategic Questions Answered:
1. **Acquisition Efficiency:** Which marketing channels and advertising campaigns generate the most profitable customers?
2. **Attribution Specialization:** How does channel return shift when evaluated under First-Touch (origin) versus Last-Touch (closing) attribution?
3. **Merchandise Demand:** Which products and categories drive top-line revenue, and which maintain the highest realized gross margins?
4. **Customer Retention:** What percentage of newly acquired buyers place repeat orders, and how does customer retention evolve across monthly cohorts?
5. **Customer Segmentation:** Which behavioral segments (VIP Champions, Loyalists, At-Risk High Value) represent the highest revenue exposure and lifetime value?
6. **Funnel Friction:** At which stage of the shopping journey (browse, product view, cart add, checkout) do prospective buyers abandon, and how does conversion vary by device?
7. **Promotional Discipline:** How severely do clearance discount bands erode realized gross margins compared to full-price orders?
8. **Supply Chain Risks:** Which hero SKUs have breached safety stock thresholds and face imminent stockout risks?

---

## 3. Technology Stack & Architecture
- **Backend & Analytics:** Python 3.10+, Pandas, NumPy, Scikit-learn, SQLite 3, SQL.
- **Frontend & Visualization:** Streamlit (Multi-page architecture), Plotly Python, Custom SaaS CSS.
- **Data Engineering:** Reproducible synthetic data generation (`scripts/generate_data.py`), automated relational schema builder (`scripts/build_database.py`).
- **Testing & Quality Assurance:** Pytest (automated data-quality, calculation, and database test suites).
- **Design System:** Bespoke luxury visual identity (Warm ivory `#FFFDF9`, Deep burgundy `#4B2634`, Muted taupe `#8C7A6B`, Champagne-gold `#C5A059`).

---

## 4. Deliverables & Artifacts
1. **Interactive Multi-Page Streamlit Dashboard:**
   - Strategic Launchpad (`app.py`)
   - 01 Executive Overview (`pages/01_Executive_Overview.py`)
   - 02 Marketing Performance (`pages/02_Marketing_Performance.py`)
   - 03 Customer Intelligence (`pages/03_Customer_Intelligence.py`)
   - 04 Product Analytics (`pages/04_Product_Analytics.py`)
   - 05 Conversion Funnel (`pages/05_Conversion_Funnel.py`)
   - 06 Cohort Analysis (`pages/06_Cohort_Analysis.py`)
   - 07 Data Quality & Governance (`pages/07_Data_Quality.py`)
2. **Relational Database & Analytical Queries:**
   - DDL Schema with Foreign Key enforcement and B-Tree indexes (`sql/schema.sql`).
   - Production SQL analytical queries covering MoM trends, RFM scoring, cohort retention, and attribution (`sql/analysis_queries.sql`).
3. **Python Analytics Library (`src/`):**
   - Ingestion and validation (`src/data/`)
   - Mathematical calculations (`src/analytics/`)
   - Database manager (`src/database/`)
   - Custom Plotly styling (`src/visualisation/`)
4. **Comprehensive Documentation Suite (`docs/` & Root):**
   - `README.md`, `REFERENCES.md`, `DATA_DICTIONARY.md`, `METRIC_DICTIONARY.md`, `METHODOLOGY.md`, `BUSINESS_INSIGHTS.md`, `USER_GUIDE.md`.

---

## 5. Governance & Synthetic Data Disclaimer
All customer names, geographic records, transaction histories, advertising spends, and inventory snapshots included in GrowthIQ are **100% synthetically generated** for portfolio demonstration purposes. The project does not claim access to any proprietary corporate databases or confidential internal systems.

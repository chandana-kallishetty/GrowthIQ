# GrowthIQ — Platform User Guide

Welcome to **GrowthIQ**, an end-to-end e-commerce marketing intelligence platform designed for fashion and athleisure D2C brands. This guide provides step-by-step instructions for launching, navigating, filtering, and exporting data from the platform.

---

## 1. Quick Start & Execution

### Prerequisites
- Python 3.10, 3.11, 3.12, 3.13, or 3.14.
- Installed virtual environment (`.venv`).

### Launching the Dashboard
Open your terminal in the `GrowthIQ` directory and run:

```bash
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
streamlit run app.py

# Windows Command Prompt
.venv\Scripts\activate.bat
streamlit run app.py

# macOS / Linux
source .venv/bin/activate
streamlit run app.py
```

Streamlit will print the local server URL (typically `http://localhost:8501`). Open this address in any modern web browser.

---

## 2. Global Interactive Controls & Sidebar

The sidebar is accessible on every page and controls global data filtering across all analytical calculations:

1. **Brand Wordmark & Nav:** Located at the top of the sidebar.
2. **Order Date Range Picker:**
   - Filters transactions between selected start and end dates.
   - Adjusts all revenue, order, and cohort calculations dynamically.
3. **Acquisition Channel Multiselect:**
   - Select or deselect individual channels (`Paid Social`, `Paid Search`, `Influencer`, `Email`, `Organic Search`, `Direct`).
   - Enables channel-isolated unit economic evaluation.
4. **Product Category Multiselect:**
   - Filter transactions and inventory across specific fashion categories (`Leggings`, `Sports Bras`, `Shorts`, `Flared Pants`, `Tops & Tanks`, `Jackets`, `Swimwear`, `Joggers`).
5. **Reset All Filters Button:**
   - Instantly restores default full-calendar-year parameters.
6. **Data Governance Notice:**
   - Reminds users that all data is synthetic for portfolio demonstration purposes.

---

## 3. Page-by-Page Analytical Walkthrough

### Home (`app.py`)
- **Purpose:** Central strategic cockpit and platform directory.
- **Key Features:**
  - Executive KPI ribbon (Revenue, Orders, AOV, ROAS, CAC, Repeat Share).
  - Navigation matrix cards providing one-click access to all 7 specialized modules.
  - End-to-end data pipeline architectural diagram.

---

### Page 1: Executive Overview (`01_Executive_Overview.py`)
- **Purpose:** Commercial velocity and board-level health indicators.
- **Key Visualizations:**
  - **Monthly Net Revenue & Gross Profit Trend:** Dual-line time series tracking commercial expansion.
  - **Category Contribution Mix:** Donut chart showing revenue share by merchandise category.
- **Actionable Tables:**
  - **Monthly Trajectory Table:** Displays completed orders, units, net sales, realized margin %, and MoM growth rate with CSV export.
- **Strategic Highlights:** Automated callout box highlighting peak revenue months and category performance.

---

### Page 2: Marketing Performance (`02_Marketing_Performance.py`)
- **Purpose:** Multi-touch acquisition efficiency, campaign economics, and attribution comparisons.
- **Key Visualizations:**
  - **Attribution Comparison (Grouped Bar):** Compares First-Touch (origin) revenue versus Last-Touch (converting) revenue by channel.
  - **Spend vs. Revenue Bubble Plot:** Bubble radius represents order volume; axes show media spend vs attributed sales.
- **Actionable Tables:**
  - **Channel Attribution Breakdown:** ROAS, CAC, orders, and variance ($\text{LT} - \text{FT}$) identifying "Closers" vs "Introducers".
  - **Campaign-Level Table:** Granular spend, impressions, clicks, CTR %, CPC, orders, and campaign ROAS.

---

### Page 3: Customer Intelligence (`03_Customer_Intelligence.py`)
- **Purpose:** Behavioral segmentation and lifetime value optimization.
- **Key Visualizations:**
  - **RFM Landscape Scatter:** Recency (days ago) plotted against Monetary Value (INR), sized by Frequency and colored by customer segment.
  - **Revenue by Customer Segment:** Bar chart displaying revenue contribution by value tier.
- **Machine Learning Section:**
  - **K-Means Clustering:** Standardized 4-cluster segmentation discovering customer personas (*High-Value Frequent*, *Dormant / Churned*, *Recent Single-Order*, *Nurturable Active*).

---

### Page 4: Product Analytics (`04_Product_Analytics.py`)
- **Purpose:** Merchandising performance, price elasticity, and stockout risk monitoring.
- **Key Visualizations:**
  - **Top Bestselling Products:** Horizontal bar chart ranking SKUs by realized revenue.
  - **Discount Band Elasticity:** Dual-axis chart comparing order volume against realized gross margin % across discount tiers (Full Price 0%, Light 1-10%, Moderate 11-20%, Clearance >20%).
- **Inventory Watchlist:**
  - Evaluates on-hand stock against safety thresholds. Highlights `CRITICAL`, `REORDER`, and `HEALTHY` items with recommended reorder quantities.

---

### Page 5: Conversion Funnel (`05_Conversion_Funnel.py`)
- **Purpose:** Milestone user progression and friction diagnostics.
- **Key Visualizations:**
  - **Interactive Funnel:** Step-by-step progression from `Sessions` $\to$ `Product Views` $\to$ `Add to Cart` $\to$ `Checkout Initiated` $\to$ `Purchases`.
  - **Device Disparity Bar:** Conversion rate differences across Mobile, Desktop, and Tablet visitors.

---

### Page 6: Cohort Analysis (`06_Cohort_Analysis.py`)
- **Purpose:** Longitudinal customer retention and lifecycle repeat purchase cadence.
- **Key Visualizations:**
  - **Triangular Retention Heatmap:** Displays retention rates from Month 0 through Month 11 for each monthly acquisition cohort.
- **Tabbed Matrices:**
  - Retention Rate (%) Matrix
  - Active Buyer Counts Matrix
  - Cumulative Cohort Revenue (INR) Trajectory

---

### Page 7: Data Quality & Governance (`07_Data_Quality.py`)
- **Purpose:** Automated pipeline validation and data integrity assurance.
- **Key Features:**
  - **Suite Status Card:** Overall pass rate (100%), total audits, zero broken constraints.
  - **Tabbed Audits:** Primary key uniqueness checks, foreign key referential integrity checks, domain constraints, and table memory profiles.
  - **Interactive Table Inspector:** Inspect raw records and schemas for any table in the database.

---

## 4. Exporting Data to CSV

Every major analytical table features a dedicated **📥 Download CSV** button in its header. Clicking the button immediately generates and downloads a clean, RFC-4180 compliant CSV file suitable for presentation, Excel modeling, or import into BI tools (Power BI, Looker, Tableau).

---

## 5. Command-Line Utilities

### Running Automated Pytest Tests
```bash
.\.venv\Scripts\python.exe -m pytest tests -v
```

### Re-generating Synthetic Data
```bash
.\.venv\Scripts\python.exe scripts\generate_data.py
```

### Re-building the SQLite Relational Database
```bash
.\.venv\Scripts\python.exe scripts\build_database.py
```


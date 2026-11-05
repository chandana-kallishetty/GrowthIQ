# GrowthIQ Technical & Analytical References

This document records the official technical documentation, API specifications, and analytical methodologies supporting the implementation of the GrowthIQ platform.

---

## 1. Technical Frameworks & Libraries

### Streamlit
- **Source title:** Streamlit Documentation & API Reference
- **Organisation:** Snowflake Inc. / Streamlit
- **Direct URL:** [https://docs.streamlit.io/](https://docs.streamlit.io/)
- **Implementation support:** Multi-page dashboard architecture (`pages/`), interactive input controls (date pickers, multiselects), session caching (`@st.cache_data`), responsive layout grids, and custom CSS theming.

### Python
- **Source title:** Python 3 Language Reference & Standard Library
- **Organisation:** Python Software Foundation
- **Direct URL:** [https://docs.python.org/3/](https://docs.python.org/3/)
- **Implementation support:** Modern standard library features, type hinting (`typing`), object-oriented modular design, date arithmetic (`datetime`), and reproducible random seed management (`random`).

### Pandas
- **Source title:** Pandas User Guide & API Reference
- **Organisation:** Pandas Development Team / NumFOCUS
- **Direct URL:** [https://pandas.pydata.org/docs/](https://pandas.pydata.org/docs/)
- **Implementation support:** Data ingestion, groupby aggregations, cohort matrix pivoting, datetime parsing, quantile scoring (`pd.qcut`), and DataFrame filtering.

### Plotly
- **Source title:** Plotly Python Open Source Graphing Library
- **Organisation:** Plotly Technologies Inc.
- **Direct URL:** [https://plotly.com/python/](https://plotly.com/python/)
- **Implementation support:** Custom themed visualization suite (`src/visualisation/charts.py`), interactive funnel charts, cohort retention heatmaps, grouped attribution bar charts, and dual-axis time series.

### Scikit-Learn
- **Source title:** Scikit-learn: Machine Learning in Python
- **Organisation:** Scikit-learn Consortium / Inria
- **Direct URL:** [https://scikit-learn.org/stable/](https://scikit-learn.org/stable/)
- **Implementation support:** Unsupervised customer clustering (`sklearn.cluster.KMeans`), feature standardization (`sklearn.preprocessing.StandardScaler`), and elbow inertia evaluation.

### SQLite
- **Source title:** SQLite Documentation & SQL Syntax
- **Organisation:** SQLite Consortium
- **Direct URL:** [https://www.sqlite.org/docs.html](https://www.sqlite.org/docs.html/)
- **Implementation support:** Relational DDL schema (`sql/schema.sql`), foreign key enforcement (`PRAGMA foreign_keys = ON;`), WAL mode, performance B-tree indexing, and analytical queries (`sql/analysis_queries.sql`).

---

## 2. Platform APIs & Analytics Industry Standards

### Google Analytics 4 (GA4)
- **Source title:** GA4 Measurement Protocol & Recommended Events
- **Organisation:** Google LLC
- **Direct URL:** [https://developers.google.com/analytics](https://developers.google.com/analytics)
- **Implementation support:** E-commerce funnel telemetry taxonomy (`session_start`, `view_item`, `add_to_cart`, `begin_checkout`, `purchase`), event-driven session models, and session attribution mechanics.

### Google BigQuery
- **Source title:** Google BigQuery Export for Google Analytics 4 Schema
- **Organisation:** Google Cloud
- **Direct URL:** [https://cloud.google.com/bigquery/docs](https://cloud.google.com/bigquery/docs)
- **Implementation support:** SQL analytical design patterns: Common Table Expressions (CTEs), window functions (`ROW_NUMBER()`, `NTILE()`, `LAG()`), and partitioned session event deduplication.

### Shopify Analytics
- **Source title:** Shopify Help Center — Analytics and Financial Metrics
- **Organisation:** Shopify Inc.
- **Direct URL:** [https://help.shopify.com/en/manual/reports-and-analytics](https://help.shopify.com/en/manual/reports-and-analytics)
- **Implementation support:** E-commerce commercial KPI definitions: Gross Sales, Net Sales (adjusting for returns and cancellations), Average Order Value (AOV), and repeat customer calculation formulas.

### Meta Marketing API
- **Source title:** Meta Marketing API Reference (Insights & Reporting)
- **Organisation:** Meta Platforms, Inc.
- **Direct URL:** [https://developers.facebook.com/docs/marketing-apis/](https://developers.facebook.com/docs/marketing-apis/)
- **Implementation support:** Advertising metrics: Impressions, Clicks, Click-Through Rate (CTR), Cost Per Click (CPC), Cost Per Mille (CPM), and Campaign Spend reporting structures.

### Google Ads API
- **Source title:** Google Ads API Documentation
- **Organisation:** Google LLC
- **Direct URL:** [https://developers.google.com/google-ads/api/docs/start](https://developers.google.com/google-ads/api/docs/start)
- **Implementation support:** Search and shopping campaign taxonomy: Brand Exact, Generic Athleisure, Performance Max, and conversion tracking mechanics.

---

## 3. Marketing Analytics & Econometric Methodologies

### RFM Customer Segmentation
- **Concept:** Recency, Frequency, Monetary (RFM) Value Analysis
- **Reference:** Hughes, Arthur M. *Strategic Database Marketing: The Masterplan for Starting and Managing a Profitable, Customer-Based Marketing Program.* McGraw-Hill, 2005.
- **Implementation support:** Quantile-based score partitioning (1–4), customer persona classification (VIP Champions, Loyal Customers, At-Risk High Value, Promising Newcomers), and lifetime value tiering.

### Multi-Touch Marketing Attribution
- **Concept:** Heuristic Rules-Based Attribution (First-Touch vs. Last-Touch vs. Linear)
- **Reference:** Berman, Ron. "Beyond the Last Touch: Attribution in Online Advertising." *Marketing Science*, 37(5), 2018.
- **Implementation support:** Identification of customer journey origins (earliest session touchpoint) versus conversion closers (converting order touchpoint), quantifying channel role specialization and spend misallocation risk.

### Customer Cohort Retention Analysis
- **Concept:** Triangular Cohort Retention & Churn Dynamics
- **Reference:** Fader, Peter S., and Bruce G. S. Hardie. "How to Project Customer Retention." *Journal of Interactive Marketing*, 21(1), 2007.
- **Implementation support:** Longitudinal grouping of customers by first purchase month, tracking active buyers across subsequent tenure intervals (M0 through M11), and cumulative cohort revenue tracking.

### Unit Economics & Incremental Lift
- **Concept:** Return on Ad Spend (ROAS) and Customer Acquisition Cost (CAC)
- **Reference:** Farris, Paul W., et al. *Marketing Metrics: The Definitive Guide to Measuring Marketing Performance.* Pearson Education, 2021.
- **Implementation support:** Clear differentiation between blended platform metrics and channel-attributed metrics, avoiding misleading conflation of correlation with causal advertising lift.

---

## 4. Integration Interface Note

To maintain reproducibility and eliminate credential dependencies during portfolio evaluation, GrowthIQ implements an extensible, file-based CSV/SQLite integration interface adhering directly to the schemas of GA4 and Shopify exports. No fabricated live API credentials or mock network servers are used.


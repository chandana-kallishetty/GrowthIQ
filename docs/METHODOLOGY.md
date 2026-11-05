# GrowthIQ — Analytical Methodology

This document details the analytical frameworks, mathematical models, and engineering implementations powering the GrowthIQ marketing intelligence platform.

---

## 1. Synthetic Data Generation & Simulation Engine

### 1.1 Reproducibility & Stochastic Process
To ensure 100% scientific reproducibility across testing and evaluation, all stochastic data generation is anchored to a fixed pseudo-random number generator seed (`seed = 42` using Python's `random` and NumPy's `np.random`).

### 1.2 Demographics & Behavioral Modeling
- **Geography:** Modeled on urban Indian e-commerce consumption patterns across Tier-1 and Tier-2 metros (Mumbai 22%, Bengaluru 20%, Delhi NCR 18%, Hyderabad 10%, Pune 8%, Chennai 7%, Kolkata, Ahmedabad, Jaipur, Chandigarh, Kochi).
- **Customer Personas:** Five distinct shopper archetypes (*Fitness Enthusiast*, *Casual Athleisure*, *Pilates & Yoga Regular*, *High-Intensity Athlete*, *Trend-Conscious Shopper*) with parameterized purchase frequencies and category affinities.
- **Seasonality Multipliers:** Incorporates festive sales surges typical in the Indian retail calendar (Q4 Diwali, festive gifting, and winter fitness campaigns exhibiting a 25%–45% volume lift).

### 1.3 Event Sequencing & Monotonic Timestamps
Event telemetry strictly models Google Analytics 4 (GA4) event sequences. Every converted order journey possesses a monotonic, chronological event progression:
$$\text{session\_start} \longrightarrow \text{view\_item} \longrightarrow \text{add\_to\_cart} \longrightarrow \text{begin\_checkout} \longrightarrow \text{purchase}$$
Each event increment has a randomized positive delay interval (20–180 seconds), ensuring zero timestamp anomalies or out-of-order events.

---

## 2. RFM Customer Segmentation Methodology

### 2.1 Feature Definitions
For every unique purchasing customer $i$, three foundational behavioral dimensions are computed from completed transaction records:
1. **Recency ($R_i$):** Elapsed days between the customer's most recent order date and the global dataset reference date ($T_{\text{ref}} = \max(T_{\text{orders}}) + 1 \text{ day}$):
   $$R_i = T_{\text{ref}} - \max(t_{i, j})$$
2. **Frequency ($F_i$):** Total count of distinct completed orders placed by customer $i$:
   $$F_i = \text{COUNT}(\text{DISTINCT } \text{order\_id}_i)$$
3. **Monetary ($M_i$):** Total cumulative net revenue realized from customer $i$:
   $$M_i = \sum_{j} \text{revenue}_{i, j}$$

### 2.2 Quantile Scoring (1–4)
To eliminate sensitivity to arbitrary cutoff values and ensure robust handling of right-skewed distributions, scores from 1 to 4 are assigned using empirical quartile ranking (`pandas.qcut` with `rank(method="first")`):
- **$R$-Score:** Inverted rank such that lower recency days receive higher scores ($4 = \text{most recent}$, $1 = \text{least recent}$).
- **$F$-Score:** Standard quartile ranking ($4 = \text{most frequent}$, $1 = \text{least frequent}$).
- **$M$-Score:** Standard quartile ranking ($4 = \text{highest cumulative spend}$, $1 = \text{lowest cumulative spend}$).

### 2.3 Segment Assignment Rules Matrix

| Customer Segment | Scoring Logic | Behavioral Characteristics | Recommended Strategy |
|---|---|---|---|
| **VIP Champions** | $M = 4 \land F \ge 3$ | Highest spenders, frequent orders, recent activity | White-glove concierge, early drop access, referral incentives |
| **Loyal Customers** | $F \ge 3$ | Consistent repeat purchasing cadence | Brand advocacy programs, tiered loyalty perks |
| **Promising Newcomers** | $R \ge 3 \land F = 1$ | Recent first-time buyers with high potential | 14-day post-purchase nurture flow, complementary cross-sells |
| **Potential Loyalists** | $R \ge 3 \land F = 2$ | Placed 2 orders recently; priming for habituation | Product recommendation bundles, review rewards |
| **At-Risk High Value** | $R \le 2 \land (M \ge 3 \lor F \ge 2)$ | Formerly high-value buyers who have stopped ordering | Personalized winback incentive, product feedback survey |
| **Hibernating / Lapsed** | $R = 1$ | Dormant customers with no recent engagement | Re-engagement email series or audience exclusion to save ad spend |
| **Active Regulars** | All other active buyers | Steady occasional purchasers | Seasonal promotional announcements |

---

## 3. Unsupervised K-Means Machine Learning Clustering

### 3.1 Preprocessing & Log-Transformation
Customer transaction metrics (especially monetary spend and order frequency) exhibit extreme positive right-skewness following Pareto power-law distributions. Feeding raw values directly into Euclidean distance-based algorithms biases clusters heavily toward extreme outliers.

We apply a monotonic log-plus-one transform:
$$x^* = \ln(1 + x) \quad \forall x \in \{R, F, M\}$$

### 3.2 Feature Standardization
Following log transformation, features are centered to zero mean and scaled to unit variance using Scikit-Learn's `StandardScaler`:
$$z = \frac{x^* - \mu}{\sigma}$$

### 3.3 Algorithm & Centroid Characterization
$k$-Means clustering partitions the standardized 3D feature space into $k=4$ non-overlapping spherical Voronoi cells by minimizing within-cluster sum of squared errors (inertia):
$$J = \sum_{k=1}^{K} \sum_{i \in C_k} \| z_i - \mu_k \|^2$$
Resulting clusters are mapped to commercial personas (*High-Value Frequent*, *Dormant / Churned*, *Recent Single-Order*, *Nurturable Active*) based on centroid coordinates.

---

## 4. Multi-Touch Marketing Attribution Comparison

### 4.1 First-Touch (FT) vs. Last-Touch (LT)
- **First-Touch Rule:** For each customer, the chronological first session visit is extracted from web telemetry. All subsequent completed orders and lifetime revenue from that customer are credited to the first touchpoint channel.
- **Last-Touch Rule:** Order revenue is credited directly to the channel stored on the converting order record.

### 4.2 Strategic Role Identification
By computing the revenue variance ($\Delta = \text{Revenue}_{\text{LT}} - \text{Revenue}_{\text{FT}}$), each channel's functional role across the consumer conversion path is quantified:
- **$\Delta > +₹50,000$ (Conversion Closer):** Channels such as Email Marketing and Direct capture substantially higher credit in Last-Touch than First-Touch, demonstrating high closing power.
- **$\Delta < -₹50,000$ (Discovery Introducer):** Channels such as Paid Social (Meta Ads) and Influencer Marketing capture significantly more credit in First-Touch than Last-Touch, proving their value as top-of-funnel customer originators.
- **Balanced Touchpoint:** Channels where First-Touch and Last-Touch contributions are approximately equal.

### 4.3 Methodological Caveats & Causal Lift
Rules-based heuristic attribution models (both FT and LT) measure correlation across recorded touchpoints; they do **not** establish counterfactual incrementality. To determine true incremental return, marketing teams must pair observational attribution with randomized controlled experiments (geo-lift testing, ad holdouts, and post-purchase surveys).

---

## 5. Triangular Cohort Retention Modeling

### 5.1 Cohort Formation
Customers are assigned to acquisition cohorts $C_m$ based on the calendar month $m \in \{\text{2025-01}, \dots, \text{2025-12}\}$ of their initial completed order.

### 5.2 Tenure Indexing
For every subsequent transaction occurring in calendar month $m_{\text{order}}$, the tenure period index $t$ is computed as:
$$t = (\text{Year}_{\text{order}} - \text{Year}_{\text{cohort}}) \times 12 + (\text{Month}_{\text{order}} - \text{Month}_{\text{cohort}})$$

### 5.3 Retention Rate Matrix
The retention rate $R(C_m, t)$ is defined as:
$$R(C_m, t) = \frac{\text{Unique Purchasing Customers from } C_m \text{ in Period } t}{\text{Initial Cohort Size } |C_m|}$$
By definition, $R(C_m, 0) = 1.0$ (100%). Unobserved future periods for younger cohorts are treated as right-censored null values.


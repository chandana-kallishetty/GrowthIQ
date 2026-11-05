# GrowthIQ — Metric Dictionary

This document provides rigorous mathematical definitions, operational grains, business rationales, and analytical caveats for every metric reported across the GrowthIQ intelligence platform.

---

## 1. Commercial & Financial KPIs

### Gross Revenue
- **Formula:** $\sum (\text{selling\_unit\_price\_inr} \times \text{quantity})$
- **Grain:** Order Item level
- **Description:** Total invoice value generated across all placed customer orders prior to deductions for returns or cancellations.
- **Caveat:** Does not represent realized cash if customer refunds occur.

### Net Realized Revenue
- **Formula:** $\sum_{\text{status} = \text{'Completed'}} (\text{selling\_unit\_price\_inr} \times \text{quantity})$
- **Grain:** Order Item level
- **Description:** Commercial revenue realized from fulfilled orders excluding refunded or cancelled orders.
- **Caveat:** Uses line-item selling price after promotional discounts.

### Completed Orders
- **Formula:** $\text{COUNT}(\text{DISTINCT } \text{order\_id}) \text{ where } \text{order\_status} = \text{'Completed'}$
- **Grain:** Order level
- **Description:** Total volume of orders successfully processed and delivered to customers.

### Average Order Value (AOV)
- **Formula:** $\frac{\text{Net Realized Revenue}}{\text{Completed Orders}}$
- **Grain:** Aggregated period / channel / segment
- **Description:** Average monetary spend per completed transaction basket.
- **Caveat:** Highly sensitive to promotional discounting and bundle packaging.

### Realized Gross Profit
- **Formula:** $\sum (\text{selling\_unit\_price\_inr} - \text{unit\_cost\_inr}) \times \text{quantity}$
- **Grain:** Order Item level
- **Description:** Commercial margin remaining after deducting product cost of goods sold (COGS).
- **Caveat:** Excludes inbound shipping, payment gateway fees, and warehousing labor unless explicitly factored into unit cost.

### Realized Gross Margin (%)
- **Formula:** $\frac{\text{Realized Gross Profit}}{\text{Net Realized Revenue}} \times 100$
- **Grain:** Aggregated period / product / category
- **Description:** Percentage of sales revenue retained as gross earnings.

### Month-over-Month (MoM) Revenue Growth (%)
- **Formula:** $\frac{\text{Revenue}_{t} - \text{Revenue}_{t-1}}{\text{Revenue}_{t-1}} \times 100$
- **Grain:** Monthly aggregation
- **Description:** Velocity of top-line revenue expansion or contraction relative to the preceding calendar month.

---

## 2. Marketing & Acquisition Unit Economics

### Marketing Expenditure (Spend)
- **Formula:** $\sum \text{spend\_inr}$
- **Grain:** Daily campaign / channel level
- **Description:** Total capital deployed across paid media platforms (Meta Ads, Google Ads, Influencer fees, lifecycle ESP tooling).

### Return on Advertising Spend (ROAS)
- **Formula:** $\frac{\text{Attributed Revenue}}{\text{Marketing Expenditure}}$
- **Grain:** Channel / Campaign level
- **Description:** Efficiency multiple indicating revenue generated per currency unit of advertising deployed.
- **Caveats:**
  - *Blended ROAS* divides total net revenue by total marketing spend.
  - *Channel Attributed ROAS* depends on the attribution model (First-Touch vs. Last-Touch). It is a correlation metric, not an experimental causal lift metric.

### Customer Acquisition Cost (CAC)
- **Formula:** $\frac{\text{Acquisition Marketing Spend}}{\text{Unique Acquired Customers}}$
- **Grain:** Channel / Period level
- **Description:** Average capital deployed to acquire a single purchasing customer.
- **Caveat:** Blended CAC includes non-paid organic/direct purchasers in the denominator unless filtered strictly to paid acquisition channels.

### Click-Through Rate (CTR %)
- **Formula:** $\frac{\text{Clicks}}{\text{Impressions}} \times 100$
- **Grain:** Daily campaign level
- **Description:** Ratio of audience clicks to total served advertising impressions. Measures creative resonance.

### Cost Per Click (CPC)
- **Formula:** $\frac{\text{Marketing Spend}}{\text{Clicks}}$
- **Grain:** Campaign / Channel level
- **Description:** Average unit cost incurred per consumer traffic click.

### Cost Per Mille (CPM)
- **Formula:** $\frac{\text{Marketing Spend}}{\text{Impressions}} \times 1000$
- **Grain:** Campaign / Channel level
- **Description:** Cost incurred to deliver 1,000 advertising impressions. Measures advertising inventory auction competitiveness.

---

## 3. Marketing Attribution Models

### First-Touch Attribution (FT)
- **Formula:** Revenue assigned to the channel/campaign of the customer's *earliest recorded website session*.
- **Business Rationale:** Identifies which channels act as the primary discovery engines and top-of-funnel customer introducers.
- **Limitation:** Ignores mid-funnel retargeting and lifecycle email closing touchpoints.

### Last-Touch Attribution (LT)
- **Formula:** Revenue assigned to the channel/campaign of the *converting order session*.
- **Business Rationale:** Identifies which touchpoints directly trigger the checkout transaction.
- **Limitation:** Systematically over-credits conversion closers (Email, Direct, Brand Search) and under-values prospecting media (Paid Social, Influencer).

---

## 4. Customer Behavioral & Retention Metrics

### Repeat Customer Share (%)
- **Formula:** $\frac{\text{Customers with } \ge 2 \text{ Completed Orders}}{\text{Total Purchasing Customers}} \times 100$
- **Grain:** Cohort / Period level
- **Description:** Proportion of buyer base that has completed more than one transaction. Key indicator of product satisfaction and loyalty.

### Customer Lifetime Value Proxy (CLV)
- **Formula:** $\frac{\text{Total Cumulative Revenue from Customer}}{\text{1}}$
- **Grain:** Individual customer level
- **Description:** Total historical spend generated by a customer over their observed lifetime.

### Cohort Retention Rate (%)
- **Formula:** $\frac{\text{Active Purchasing Customers in Month } M_t}{\text{Original Initial Buyers in Month } M_0} \times 100$
- **Grain:** Cohort Month $\times$ Period tenure month ($t = 0, 1, 2, \dots, 11$)
- **Description:** Percentage of an acquisition cohort that returns to place at least one order in tenure month $t$.

---

## 5. E-Commerce Funnel Telemetry

### Session-to-Product-View Rate (%)
- **Formula:** $\frac{\text{Unique Sessions with } \text{'view\_item'}}{\text{Unique Sessions with } \text{'session\_start'}} \times 100$
- **Description:** Proportion of incoming visits that browse at least one product detail page.

### Product-View-to-Cart Rate (%)
- **Formula:** $\frac{\text{Unique Sessions with } \text{'add\_to\_cart'}}{\text{Unique Sessions with } \text{'view\_item'}} \times 100$
- **Description:** Efficacy of merchandising, product photography, and pricing in driving purchase intent.

### Cart-to-Checkout Rate (%)
- **Formula:** $\frac{\text{Unique Sessions with } \text{'begin\_checkout'}}{\text{Unique Sessions with } \text{'add\_to\_cart'}} \times 100$
- **Description:** Proportion of carting visitors who initiate the payment and shipping flow.

### Checkout-to-Purchase Rate (%)
- **Formula:** $\frac{\text{Unique Sessions with } \text{'purchase'}}{\text{Unique Sessions with } \text{'begin\_checkout'}} \times 100$
- **Description:** Checkout flow completion rate; inversely measures payment failures, shipping sticker shock, and UX friction.

### Overall Session Conversion Rate (%)
- **Formula:** $\frac{\text{Completed Orders}}{\text{Total Browsing Sessions}} \times 100$
- **Description:** End-to-end commercial conversion rate of traffic into paid orders.

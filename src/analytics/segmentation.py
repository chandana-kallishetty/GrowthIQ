"""
GrowthIQ Customer Segmentation & RFM Clustering Module
------------------------------------------------------
Implements RFM (Recency, Frequency, Monetary) segmentation and unsupervised
K-Means clustering to uncover distinct customer behavioural personas.
"""

from typing import Dict, Any, Tuple
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from src.analytics.kpis import order_facts


def calculate_rfm(orders: pd.DataFrame, items: pd.DataFrame) -> pd.DataFrame:
    """
    Computes individual customer-level Recency, Frequency, and Monetary (RFM) metrics.
    """
    facts = order_facts(orders, items)
    if facts.empty:
        return pd.DataFrame()

    completed = facts[facts["order_status"] == "Completed"] if "order_status" in facts.columns else facts
    if completed.empty:
        return pd.DataFrame()

    if not pd.api.types.is_datetime64_any_dtype(completed["order_date"]):
        completed["order_date"] = pd.to_datetime(completed["order_date"])

    max_dt = pd.to_datetime(completed["order_date"].max())
    reference_date = max_dt + pd.DateOffset(days=1)

    rfm = (
        completed.groupby("customer_id")
        .agg(
            last_order_date=("order_date", "max"),
            first_order_date=("order_date", "min"),
            frequency=("order_id", "nunique"),
            monetary_inr=("revenue_inr", "sum"),
            gross_profit_inr=("gross_profit_inr", "sum"),
            units_bought=("units", "sum"),
        )
        .reset_index()
    )

    rfm["recency_days"] = (reference_date - rfm["last_order_date"]).dt.days
    rfm["customer_tenure_days"] = (reference_date - rfm["first_order_date"]).dt.days
    rfm["aov_inr"] = rfm["monetary_inr"] / rfm["frequency"]

    # Assign quantile scores (1 to 4)
    # Recency: lower days is better, so invert score
    rfm["r_score"] = pd.qcut(
        rfm["recency_days"].rank(method="first", ascending=False),
        q=4,
        labels=[1, 2, 3, 4],
    ).astype(int)

    rfm["f_score"] = pd.qcut(
        rfm["frequency"].rank(method="first"),
        q=4,
        labels=[1, 2, 3, 4],
    ).astype(int)

    rfm["m_score"] = pd.qcut(
        rfm["monetary_inr"].rank(method="first"),
        q=4,
        labels=[1, 2, 3, 4],
    ).astype(int)

    # Segment Assignment Matrix
    def assign_segment(row):
        r, f, m = row["r_score"], row["f_score"], row["m_score"]
        if m == 4 and f >= 3:
            return "VIP Champions"
        elif f >= 3:
            return "Loyal Customers"
        elif r >= 3 and f == 1:
            return "Promising Newcomers"
        elif r >= 3 and f == 2:
            return "Potential Loyalists"
        elif r <= 2 and (m >= 3 or f >= 2):
            return "At-Risk High Value"
        elif r == 1:
            return "Hibernating / Lapsed"
        else:
            return "Active Regulars"

    rfm["segment"] = rfm.apply(assign_segment, axis=1)
    return rfm


def cluster_customers_kmeans(
    rfm_df: pd.DataFrame, n_clusters: int = 4, random_state: int = 42
) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Applies K-Means clustering with feature standardisation to discover customer personas.
    Handles skewness and edge cases gracefully.
    """
    if rfm_df.empty or len(rfm_df) < n_clusters:
        return rfm_df, {"error": "Insufficient customer volume for K-Means clustering"}

    df = rfm_df.copy()
    features = ["recency_days", "frequency", "monetary_inr"]

    # Log-transform right-skewed features for robust Gaussian-like distance computation
    features_log = np.log1p(df[features].values)

    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(features_log)

    kmeans = KMeans(n_clusters=n_clusters, random_state=random_state, n_init=10)
    df["cluster"] = kmeans.fit_predict(scaled_data)

    # Calculate cluster profiles
    cluster_profiles = (
        df.groupby("cluster")
        .agg(
            customer_count=("customer_id", "count"),
            avg_recency=("recency_days", "mean"),
            avg_frequency=("frequency", "mean"),
            avg_spend=("monetary_inr", "mean"),
            total_revenue=("monetary_inr", "sum"),
        )
        .reset_index()
    )

    # Assign meaningful business names based on spend & frequency centroids
    def label_cluster(row):
        if row["avg_spend"] > cluster_profiles["avg_spend"].median() and row["avg_frequency"] >= 2.0:
            return "High-Value Frequent"
        elif row["avg_recency"] > cluster_profiles["avg_recency"].median():
            return "Dormant / Churned"
        elif row["avg_frequency"] <= 1.2:
            return "Recent Single-Order"
        else:
            return "Nurturable Active"

    cluster_profiles["persona_label"] = cluster_profiles.apply(label_cluster, axis=1)
    cluster_map = dict(zip(cluster_profiles["cluster"], cluster_profiles["persona_label"]))
    df["cluster_label"] = df["cluster"].map(cluster_map)

    summary = {
        "inertia": float(kmeans.inertia_),
        "n_clusters": n_clusters,
        "cluster_profiles": cluster_profiles,
    }

    return df, summary

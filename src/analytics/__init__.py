from .kpis import order_facts, kpi_summary, monthly_kpi_trends
from .attribution import compute_attribution_models
from .segmentation import calculate_rfm, cluster_customers_kmeans
from .cohorts import build_cohort_matrices, cohort_summary_metrics
from .funnel import funnel_metrics, device_funnel_comparison
from .products import (
    product_performance,
    category_performance,
    discount_effectiveness_analysis,
    inventory_watchlist,
)

__all__ = [
    "order_facts",
    "kpi_summary",
    "monthly_kpi_trends",
    "compute_attribution_models",
    "calculate_rfm",
    "cluster_customers_kmeans",
    "build_cohort_matrices",
    "cohort_summary_metrics",
    "funnel_metrics",
    "device_funnel_comparison",
    "product_performance",
    "category_performance",
    "discount_effectiveness_analysis",
    "inventory_watchlist",
]


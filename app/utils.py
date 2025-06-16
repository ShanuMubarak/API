# Placeholder for utils.py
import pandas as pd
from collections import defaultdict
from app.config import settings

def generate_recommendation_mapping(df: pd.DataFrame, cluster_mapping: dict) -> dict:
    """Builds cluster-to-top-categories mapping based on customer cluster."""
    cluster_to_categories = defaultdict(list)

    for cluster, customers in cluster_mapping.items():
        filtered = df[df['CustomerID'].isin(customers)]
        top_categories = (
            filtered['Category']
            .value_counts()
            .head(3)
            .index
            .tolist()
        )
        cluster_to_categories[cluster] = top_categories

    return dict(cluster_to_categories)

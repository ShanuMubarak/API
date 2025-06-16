import pandas as pd

def generate_recommendation_map(csv_path: str, top_n: int = 5):
    """
    Generate a product recommendation map based on top-selling products per category.
    Returns: dict {Category: [TopProductIDs]}
    """
    try:
        df = pd.read_csv(csv_path)
        df.columns = [col.strip().replace(" ", "_") for col in df.columns]

        required_cols = {"Product_ID", "Category"}
        if not required_cols.issubset(df.columns):
            raise ValueError(f"Missing required columns: {required_cols - set(df.columns)}")

        category_top_products = (
            df.groupby(["Category", "Product_ID"])
            .size()
            .reset_index(name="count")
            .sort_values(["Category", "count"], ascending=[True, False])
        )

        recommendation_map = {}
        for category in category_top_products["Category"].unique():
            top_products = category_top_products[
                category_top_products["Category"] == category
            ].head(top_n)["Product_ID"].tolist()
            recommendation_map[category] = top_products

        return recommendation_map

    except Exception as e:
        print(f"Error generating recommendation map: {e}")
        return {}

def get_recommendations_for_category(category: str, recommendation_map: dict, num_products: int = 5):
    """Fetch top products for a given product category"""
    return recommendation_map.get(category, [])[:num_products]

def get_recommendations_for_customer(customer_id: str, csv_path: str = "merged_orders.csv", num_products: int = 5):
    """
    Recommend products for a given customer ID based on their most purchased product category.
    """
    try:
        df = pd.read_csv(csv_path)
        df.columns = [col.strip().replace(" ", "_") for col in df.columns]

        if "Customer_ID" not in df.columns or "Category" not in df.columns:
            raise ValueError("Missing required columns in merged_orders.csv")

        customer_orders = df[df["Customer_ID"] == customer_id]
        if customer_orders.empty:
            return []

        top_category = customer_orders["Category"].value_counts().idxmax()
        recommendation_map = generate_recommendation_map(csv_path, top_n=num_products)
        return get_recommendations_for_category(top_category, recommendation_map, num_products)

    except Exception as e:
        print(f"Error recommending for customer {customer_id}: {e}")
        return []

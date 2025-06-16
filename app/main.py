from fastapi import FastAPI, HTTPException
from app.schemas import (
    CustomerBatch,
    PredictionResponse,
    RecommendationRequest,
    ProductRecommendationResponse
)
from app.config import settings
from app.logger import get_logger
from app.scheduler import start, shutdown
from app.database import init_db
from app.recommender import (
    get_recommendations_for_category,
    get_recommendations_for_customer,
    generate_recommendation_map
)
import pickle
import mysql.connector
import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

#  App Initialization
app = FastAPI(title="Customer Segmentation + Recommendation API")
logger = get_logger()

model = None
scaler = None

#  Load Order Data
csv_path = "merged_orders.csv"
if not os.path.exists(csv_path):
    raise FileNotFoundError(f"{csv_path} not found. Please ensure the file is in the project root.")

order_df = pd.read_csv(csv_path)

# Normalize column names
order_df.columns = [col.strip().replace(" ", "_") for col in order_df.columns]

required_cols = {"Customer_ID", "Category"}
if not required_cols.issubset(order_df.columns):
    raise ValueError(f"CSV is missing required columns: {required_cols - set(order_df.columns)}")


#  Database Connection Helper
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DB")
    )

#  Startup and Shutdown Events
@app.on_event("startup")
def on_startup():
    global model, scaler
    logger.info("Starting up...")
    init_db()
    with open(settings.model_path, "rb") as f:
        model = pickle.load(f)
    with open(settings.scaler_path, "rb") as f:
        scaler = pickle.load(f)
    logger.info("Model and Scaler loaded.")
    start()

@app.on_event("shutdown")
def on_shutdown():
    shutdown()
    logger.info("Shutdown complete.")

#  Root Endpoint
@app.get("/", tags=["Root"])
def get_customer():
    return {"message": "API is up and running."}

#  Prediction Endpoint
@app.post("/predict", response_model=list[PredictionResponse], tags=["Prediction"])
def predict_clusters(batch: CustomerBatch):
    try:
        data = []
        ids = []
        num_recs = []

        for customer in batch.customers:
            data.append([
                customer.Total_Spent,
                customer.Total_Quantity,
                customer.Num_Orders,
                customer.Customer_Age,
                customer.Gender_Code
            ])
            ids.append(customer.CustomerID)
            num_recs.append(customer.Num_Recommendations)

        scaled = scaler.transform(data)
        predictions = model.predict(scaled)

        recommendation_map = generate_recommendation_map(csv_path)

        results = []
        for customer_id, cluster, n in zip(ids, predictions, num_recs):
            category = str(cluster)
            products = get_recommendations_for_category(category, recommendation_map, n)
            results.append(PredictionResponse(
                customer_id=customer_id,
                cluster=cluster,
                recommended_products=products
            ))

        return results
    except Exception as e:
        logger.exception("Prediction failed")
        raise HTTPException(status_code=500, detail="Prediction failed")

#  Recommend by Customer ID
@app.post("/recommend_by_customer_id", response_model=ProductRecommendationResponse, tags=["Recommendation"])
def recommend_by_customer_id(request: RecommendationRequest):
    customer_id = request.customer_id
    num_products = request.num_products

    recommended = get_recommendations_for_customer(customer_id, csv_path, num_products)

    if not recommended:
        raise HTTPException(status_code=404, detail=f"No recommendations found for customer ID {customer_id}")

    return ProductRecommendationResponse(
        customer_id=customer_id,
        recommended_products=recommended
    )

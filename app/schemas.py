from pydantic import BaseModel
from typing import List

class CustomerData(BaseModel):
    CustomerID: str
    Total_Spent: float
    Total_Quantity: int
    Num_Orders: int
    Customer_Age: int
    Gender_Code: int
    Num_Recommendations: int = 3

class CustomerBatch(BaseModel):
    customers: List[CustomerData]

class PredictionResponse(BaseModel):
    customer_id: str
    cluster: int
    recommended_products: List[str]

class RecommendationRequest(BaseModel):
    customer_id: str
    num_products: int = 5

class ProductRecommendationResponse(BaseModel):
    customer_id: str
    recommended_products: List[str]

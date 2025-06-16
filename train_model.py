import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import pickle
import os

# Load data
df = pd.read_csv("data\merged_orders.csv")

# Standardize column names
df.columns = df.columns.str.strip().str.replace(" ", "_").str.title()
df.rename(columns={"Customer_Id": "CustomerID"}, inplace=True)

# Encode gender
df["Gender_Code"] = df["Customer_Gender"].map({"Male": 0, "Female": 1})

# Group and aggregate
agg_df = df.groupby("CustomerID").agg(
    Total_Spent=("Total_Price", "sum"),
    Total_Quantity=("Quantity", "sum"),
    Num_Orders=("Order_Id", "nunique"),
    Customer_Age=("Customer_Age", "first"),
    Gender_Code=("Gender_Code", "first")
).reset_index()

agg_df.dropna(inplace=True)

# Features
features = ["Total_Spent", "Total_Quantity", "Num_Orders", "Customer_Age", "Gender_Code"]
X = agg_df[features].values

# Scale and cluster
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

model = KMeans(n_clusters=3, random_state=42)
model.fit(X_scaled)

# Save files
os.makedirs("data/models", exist_ok=True)
with open("data/models/scaler.pkl", "wb") as f:
    pickle.dump(scaler, f)
with open("data/models/clustering_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model and scaler saved to data/models/")

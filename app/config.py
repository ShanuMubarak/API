import configparser
import os

config = configparser.ConfigParser()
config.read("config.ini")

class Settings:
    model_path = config.get("paths", "model_path", fallback="app/models/kmeans_model.pkl")
    scaler_path = config.get("paths", "scaler_path", fallback="app/models/scaler.pkl")
    data_csv_path = config.get("paths", "data_csv_path", fallback="data/merged_orders.csv")
    scheduler_interval = config.getint("scheduler", "interval_seconds", fallback=60)

settings = Settings()

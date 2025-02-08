from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import pandas as pd
import joblib
import os
import sys
sys.path.append('..')

from src.utils.feature_engineering import FeatureEngineer

app = FastAPI(title="Fraud Detection API")

# Load the trained model
MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                         'models', 'fraud_detector.joblib')
model = joblib.load(MODEL_PATH)
feature_engineer = FeatureEngineer()

class Trade(BaseModel):
    timestamp: str
    trade_amount: float
    trade_duration_seconds: float
    profit_loss: float

class Transaction(BaseModel):
    timestamp: str
    transaction_type: str
    amount: float

class UserData(BaseModel):
    user_id: int
    trades: List[Trade]
    transactions: List[Transaction]

@app.post("/predict")
async def predict_fraud(user_data: UserData):
    try:
        # Convert input data to dataframes
        trades_df = pd.DataFrame([trade.dict() for trade in user_data.trades])
        trades_df['user_id'] = user_data.user_id
        
        transactions_df = pd.DataFrame([tx.dict() for tx in user_data.transactions])
        transactions_df['user_id'] = user_data.user_id
        
        # Engineer features
        features = feature_engineer.calculate_user_features(trades_df, transactions_df)
        
        # Make prediction
        fraud_prob = model.predict_proba(features)[0][1]
        
        return {
            "user_id": user_data.user_id,
            "fraud_probability": float(fraud_prob),
            "risk_level": "high" if fraud_prob > 0.7 else "medium" if fraud_prob > 0.3 else "low"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
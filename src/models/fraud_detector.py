from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import pandas as pd
import numpy as np
import joblib

class FraudDetector:
    def __init__(self, random_state=42):
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=random_state
        )
        
    def train(self, features, labels):
        """Train the fraud detection model"""
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            features, 
            labels, 
            test_size=0.2, 
            random_state=42
        )
        
        # Train model
        self.model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = self.model.predict(X_test)
        print("\nModel Performance:")
        print(classification_report(y_test, y_pred))
        
        return {
            'X_train': X_train,
            'X_test': X_test,
            'y_test': y_test,
            'y_pred': y_pred
        }
    
    def predict(self, features):
        """Make predictions on new data"""
        return self.model.predict_proba(features)
    
    def save_model(self, filepath):
        """Save model to disk"""
        joblib.dump(self.model, filepath)
    
    @classmethod
    def load_model(cls, filepath):
        """Load model from disk"""
        instance = cls()
        instance.model = joblib.load(filepath)
        return instance
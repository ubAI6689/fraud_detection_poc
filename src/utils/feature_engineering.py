# src/utils/feature_engineering.py
import pandas as pd
import numpy as np

class FeatureEngineer:
    def __init__(self):
        pass
        
    def calculate_user_features(self, trades_df, transactions_df):
        """Calculate features for each user based on their trading and transaction patterns"""
        
        # Trading features
        trade_features = trades_df.groupby('user_id').agg({
            'trade_amount': ['count', 'mean', 'std', 'sum'],
            'trade_duration_seconds': ['mean', 'std'],
            'profit_loss': ['mean', 'std', 'sum']
        })
        
        # Flatten column names
        trade_features.columns = ['_'.join(col).strip() for col in trade_features.columns.values]
        
        # Transaction features
        deposits = transactions_df[transactions_df['transaction_type'] == 'deposit']
        withdrawals = transactions_df[transactions_df['transaction_type'] == 'withdrawal']
        
        deposit_features = deposits.groupby('user_id').agg({
            'amount': ['count', 'mean', 'sum']
        })
        deposit_features.columns = ['deposit_' + '_'.join(col).strip() 
                                  for col in deposit_features.columns.values]
        
        withdrawal_features = withdrawals.groupby('user_id').agg({
            'amount': ['count', 'mean', 'sum']
        })
        withdrawal_features.columns = ['withdrawal_' + '_'.join(col).strip() 
                                     for col in withdrawal_features.columns.values]
        
        # Combine features
        features = pd.concat([
            trade_features,
            deposit_features,
            withdrawal_features
        ], axis=1, sort=True)
        
        # Fill missing values
        features = features.fillna(0)
        
        # Calculate derived features
        features['deposit_withdrawal_ratio'] = (
            features['deposit_amount_sum'] / 
            (features['withdrawal_amount_sum'] + 1)
        )
        
        features['avg_trade_amount_per_deposit'] = (
            features['trade_amount_sum'] / 
            (features['deposit_amount_sum'] + 1)
        )
        
        features['trade_frequency'] = (
            features['trade_amount_count'] / 
            (features['deposit_amount_count'] + 1)
        )
        
        return features
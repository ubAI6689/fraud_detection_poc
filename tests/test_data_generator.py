# tests/test_data_generator.py
import pytest
from src.utils.data_generator import DataGenerator

def test_data_generator():
    generator = DataGenerator(seed=42)
    trades_df, transactions_df, labels_df = generator.generate_dataset(n_users=10)
    
    # Basic checks
    assert len(trades_df) > 0
    assert len(transactions_df) > 0
    assert len(labels_df) == 10
    
    # Check columns
    assert all(col in trades_df.columns for col in ['user_id', 'timestamp', 'trade_amount'])
    assert all(col in transactions_df.columns for col in ['user_id', 'timestamp', 'amount'])
    assert 'is_fraudulent' in labels_df.columns
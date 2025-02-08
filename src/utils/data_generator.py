import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class DataGenerator:
    def __init__(self, seed=42):
        np.random.seed(seed)
        
    def generate_user_trades(self, user_id, profile_type, num_trades=None):
        """Generate trade data based on user profile"""
        trades = []
        base_date = datetime.now() - timedelta(days=30)
        
        # Set default num_trades based on profile if not specified
        if num_trades is None:
            num_trades = {
                "Regular Trader": np.random.randint(10, 20),
                "High Volume Trader": np.random.randint(40, 60),
                "New User": np.random.randint(1, 5),
                "Suspicious Pattern": np.random.randint(15, 25),
                "Day Trader": np.random.randint(30, 50),
                "Long-term Investor": np.random.randint(3, 8)
            }.get(profile_type, 10)

        if profile_type == "High Volume Trader":
            # Frequent large trades
            for _ in range(num_trades):
                trades.append({
                    'user_id': user_id,
                    'timestamp': base_date + timedelta(hours=np.random.randint(1, 720)),
                    'trade_amount': np.random.uniform(1000, 5000),
                    'trade_duration_seconds': np.random.randint(300, 3600),
                    'profit_loss': np.random.normal(0, 500)
                })

        elif profile_type == "Suspicious Pattern":
            # Quick successive small trades
            for _ in range(num_trades):
                trades.append({
                    'user_id': user_id,
                    'timestamp': base_date + timedelta(minutes=np.random.randint(1, 30)),
                    'trade_amount': np.random.uniform(1, 10),
                    'trade_duration_seconds': np.random.randint(1, 30),
                    'profit_loss': np.random.uniform(-0.5, 0.5)
                })

        elif profile_type == "New User":
            # Few small trades
            for _ in range(num_trades):
                trades.append({
                    'user_id': user_id,
                    'timestamp': base_date + timedelta(days=np.random.randint(1, 5)),
                    'trade_amount': np.random.uniform(10, 100),
                    'trade_duration_seconds': np.random.randint(60, 3600),
                    'profit_loss': np.random.normal(0, 10)
                })

        elif profile_type == "Day Trader":
            # Multiple trades per day, medium amounts
            for _ in range(num_trades):
                trades.append({
                    'user_id': user_id,
                    'timestamp': base_date + timedelta(hours=np.random.randint(1, 720)),
                    'trade_amount': np.random.uniform(100, 1000),
                    'trade_duration_seconds': np.random.randint(60, 1800),
                    'profit_loss': np.random.normal(0, 100)
                })

        elif profile_type == "Long-term Investor":
            # Few trades, larger amounts
            for _ in range(num_trades):
                trades.append({
                    'user_id': user_id,
                    'timestamp': base_date + timedelta(days=np.random.randint(1, 30)),
                    'trade_amount': np.random.uniform(5000, 10000),
                    'trade_duration_seconds': np.random.randint(3600, 86400),
                    'profit_loss': np.random.normal(0, 1000)
                })

        else:  # Regular Trader
            # Normal distribution of trades
            for _ in range(num_trades):
                trades.append({
                    'user_id': user_id,
                    'timestamp': base_date + timedelta(hours=np.random.randint(1, 720)),
                    'trade_amount': np.random.uniform(100, 1000),
                    'trade_duration_seconds': np.random.randint(300, 3600),
                    'profit_loss': np.random.normal(0, 100)
                })
                
        return pd.DataFrame(trades)

    def generate_user_transactions(self, user_id, profile_type):
        """Generate transaction data based on user profile"""
        transactions = []
        base_date = datetime.now() - timedelta(days=30)
        
        if profile_type == "High Volume Trader":
            # Multiple large deposits and withdrawals
            num_transactions = np.random.randint(10, 15)
            for _ in range(num_transactions):
                amount = np.random.uniform(5000, 10000)
                transactions.append({
                    'user_id': user_id,
                    'timestamp': base_date + timedelta(days=np.random.randint(1, 30)),
                    'transaction_type': np.random.choice(['deposit', 'withdrawal']),
                    'amount': amount
                })

        elif profile_type == "Suspicious Pattern":
            # Large deposit followed by quick withdrawals
            deposit_amount = np.random.uniform(5000, 10000)
            transactions.append({
                'user_id': user_id,
                'timestamp': base_date,
                'transaction_type': 'deposit',
                'amount': deposit_amount
            })
            
            transactions.append({
                'user_id': user_id,
                'timestamp': base_date + timedelta(days=np.random.randint(1, 3)),
                'transaction_type': 'withdrawal',
                'amount': deposit_amount * 0.95
            })

        elif profile_type == "New User":
            # One or two small deposits
            num_transactions = np.random.randint(1, 3)
            for _ in range(num_transactions):
                transactions.append({
                    'user_id': user_id,
                    'timestamp': base_date + timedelta(days=np.random.randint(1, 5)),
                    'transaction_type': 'deposit',
                    'amount': np.random.uniform(100, 500)
                })

        else:  # Regular patterns for other profiles
            num_transactions = np.random.randint(5, 10)
            for _ in range(num_transactions):
                amount = np.random.uniform(500, 2000)
                transactions.append({
                    'user_id': user_id,
                    'timestamp': base_date + timedelta(days=np.random.randint(1, 30)),
                    'transaction_type': np.random.choice(['deposit', 'withdrawal']),
                    'amount': amount
                })
                
        return pd.DataFrame(transactions)

    def generate_dataset(self, n_users=1, profile_type="Regular Trader"):
        """Generate complete dataset for given number of users"""
        all_trades = pd.DataFrame()
        all_transactions = pd.DataFrame()
        labels = []
        
        for user_id in range(n_users):
            # Generate trades and transactions based on profile
            trades_df = self.generate_user_trades(user_id, profile_type)
            transactions_df = self.generate_user_transactions(user_id, profile_type)
            
            all_trades = pd.concat([all_trades, trades_df])
            all_transactions = pd.concat([all_transactions, transactions_df])
            
            # Determine if profile is fraudulent
            is_fraudulent = 1 if profile_type == "Suspicious Pattern" else 0
            labels.append({'user_id': user_id, 'is_fraudulent': is_fraudulent})
        
        return all_trades, all_transactions, pd.DataFrame(labels)
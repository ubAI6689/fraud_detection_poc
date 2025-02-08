# src/utils/data_generator.py
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class DataGenerator:
    def __init__(self, seed=42):
        np.random.seed(seed)
        
    def generate_user_trades(self, user_id, is_fraudulent, num_trades):
        """Generate trade data for a single user with more nuanced patterns"""
        trades = []
        base_date = datetime.now() - timedelta(days=30)
        
        if is_fraudulent:
            # Add some variance to fraudulent patterns
            trade_amounts = np.random.normal(15, 10, num_trades)  # More variance in amounts
            durations = np.random.exponential(30, num_trades)     # Mix of quick and longer trades
            
            for i in range(num_trades):
                trades.append({
                    'user_id': user_id,
                    'timestamp': base_date + timedelta(minutes=np.random.randint(1, 120)),
                    'trade_amount': max(1, trade_amounts[i]),  # Ensure positive amount
                    'trade_duration_seconds': max(1, durations[i]),
                    'profit_loss': np.random.normal(0, 2)  # More realistic P/L
                })
        else:
            # Normal trading pattern with more realistic distribution
            trade_amounts = np.random.lognormal(4, 1, num_trades)  # Log-normal distribution for amounts
            durations = np.random.lognormal(5, 1, num_trades)      # Log-normal for durations
            
            for i in range(num_trades):
                trades.append({
                    'user_id': user_id,
                    'timestamp': base_date + timedelta(hours=np.random.randint(1, 720)),
                    'trade_amount': trade_amounts[i],
                    'trade_duration_seconds': durations[i],
                    'profit_loss': np.random.normal(0, trade_amounts[i] * 0.1)  # P/L proportional to trade size
                })
        
        return trades

    def generate_user_transactions(self, user_id, is_fraudulent, num_transactions):
        """Generate more realistic transaction patterns"""
        transactions = []
        base_date = datetime.now() - timedelta(days=30)

        if is_fraudulent:
            # Add some noise to fraudulent patterns
            deposit_amount = np.random.lognormal(8, 0.5)  # More variable deposit amounts
            withdrawal_delay = np.random.exponential(2)    # Variable withdrawal timing
            withdrawal_fraction = np.random.uniform(0.85, 0.98)  # Variable withdrawal amount

            transactions.append({
                'user_id': user_id,
                'timestamp': base_date,
                'transaction_type': 'deposit',
                'amount': deposit_amount
            })

            # Maybe add some small trades in between
            if np.random.random() < 0.3:  # 30% chance of small intermediate transaction
                transactions.append({
                    'user_id': user_id,
                    'timestamp': base_date + timedelta(days=withdrawal_delay/2),
                    'transaction_type': np.random.choice(['deposit', 'withdrawal']),
                    'amount': deposit_amount * 0.1
                })

            transactions.append({
                'user_id': user_id,
                'timestamp': base_date + timedelta(days=withdrawal_delay),
                'transaction_type': 'withdrawal',
                'amount': deposit_amount * withdrawal_fraction
            })
        else:
            # Normal transaction pattern
            for _ in range(num_transactions):
                amount = np.random.lognormal(5, 1)
                transactions.append({
                    'user_id': user_id,
                    'timestamp': base_date + timedelta(days=np.random.randint(1, 30)),
                    'transaction_type': np.random.choice(
                        ['deposit', 'withdrawal'],
                        p=[0.6, 0.4]  # Slightly more deposits than withdrawals
                    ),
                    'amount': amount
                })

        return transactions

    def generate_dataset(self, n_users=1000):
        """Generate complete dataset with both fraudulent and legitimate users"""
        all_trades = []
        all_transactions = []
        user_labels = {}
        
        for user_id in range(n_users):
            # 10% of users are fraudulent
            is_fraudulent = np.random.random() < 0.1
            user_labels[user_id] = is_fraudulent
            
            if is_fraudulent:
                trades = self.generate_user_trades(user_id, True, np.random.randint(1, 5))
                transactions = self.generate_user_transactions(user_id, True, 2)
            else:
                trades = self.generate_user_trades(user_id, False, np.random.randint(10, 50))
                transactions = self.generate_user_transactions(user_id, False, np.random.randint(5, 15))
            
            all_trades.extend(trades)
            all_transactions.extend(transactions)
        
        trades_df = pd.DataFrame(all_trades)
        transactions_df = pd.DataFrame(all_transactions)
        labels_df = pd.DataFrame.from_dict(user_labels, orient='index', columns=['is_fraudulent'])
        
        return trades_df, transactions_df, labels_df
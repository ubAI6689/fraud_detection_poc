import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import json
from datetime import datetime, timedelta
import sys
import os

sys.path.append('..')
from utils.data_generator import DataGenerator

# Configure the page
st.set_page_config(
    page_title="Fraud Detection Dashboard",
    layout="wide"
)

# Title
st.title("Fraud Detection Dashboard")

# Generate sample user profiles
def generate_user_profiles():
    return {
        "Regular Trader": 1001,
        "High Volume Trader": 1002,
        "New User": 1003,
        "Suspicious Pattern": 1004,
        "Day Trader": 1005,
        "Long-term Investor": 1006
    }

# Sidebar for controls
st.sidebar.header("Controls")

# Create dropdown for user profiles
user_profiles = generate_user_profiles()
selected_profile = st.sidebar.selectbox(
    "Select User Profile",
    options=list(user_profiles.keys())
)
user_id = user_profiles[selected_profile]

def generate_sample_data(user_id, profile_type):
    """Generate sample data based on user profile"""
    generator = DataGenerator()
    
    # Generate data with profile type
    trades_df, transactions_df, _ = generator.generate_dataset(
        n_users=1, 
        profile_type=profile_type  # This should match the parameter name in DataGenerator
    )
    
    # Format for API
    trades = trades_df.to_dict('records')
    transactions = transactions_df.to_dict('records')
    
    # Convert timestamps to strings
    for trade in trades:
        trade['timestamp'] = trade['timestamp'].isoformat()
    for tx in transactions:
        tx['timestamp'] = tx['timestamp'].isoformat()
    
    return {
        "user_id": user_id,
        "trades": trades,
        "transactions": transactions
    }

if st.sidebar.button("Analyze User"):
    # Generate and send data to API
    data = generate_sample_data(user_id, selected_profile)
    
    try:
        response = requests.post(
            "http://localhost:8000/predict",
            json=data
        )
        result = response.json()
        
        # Create columns for metrics
        col1, col2, col3 = st.columns(3)
        
        # Display metrics
        with col1:
            st.metric("Fraud Probability", f"{result['fraud_probability']:.2%}")
        with col2:
            st.metric("Risk Level", result['risk_level'].upper())
        with col3:
            st.metric("Number of Transactions", 
                     len(data['trades']) + len(data['transactions']))
        
        # Create tabs for different views
        tab1, tab2 = st.tabs(["Transactions", "Trades"])
        
        with tab1:
            # Transaction timeline
            transactions_df = pd.DataFrame(data['transactions'])
            transactions_df['timestamp'] = pd.to_datetime(transactions_df['timestamp'])
            
            fig = px.scatter(transactions_df, 
                           x='timestamp', 
                           y='amount',
                           color='transaction_type',
                           title='Transaction Timeline')
            st.plotly_chart(fig, use_container_width=True)
            
            # Show raw data
            st.dataframe(transactions_df)
            
        with tab2:
            # Trade analysis
            trades_df = pd.DataFrame(data['trades'])
            trades_df['timestamp'] = pd.to_datetime(trades_df['timestamp'])
            
            fig = px.scatter(trades_df,
                           x='timestamp',
                           y='trade_amount',
                           color='profit_loss',
                           title='Trading Activity')
            st.plotly_chart(fig, use_container_width=True)
            
            # Show raw data
            st.dataframe(trades_df)
            
    except Exception as e:
        st.error(f"Error: {str(e)}")

# Add profile descriptions
st.sidebar.markdown("---")
st.sidebar.markdown(f"""
### Selected Profile: {selected_profile}
{
    {
        "Regular Trader": "Normal trading patterns with moderate activity",
        "High Volume Trader": "Frequent trades with large volumes",
        "New User": "Limited trading history, small number of transactions",
        "Suspicious Pattern": "Unusual trading patterns that may indicate fraud",
        "Day Trader": "Multiple trades per day with short holding periods",
        "Long-term Investor": "Fewer trades with longer holding periods"
    }[selected_profile]
}
""")

# Add additional information
st.sidebar.markdown("---")
st.sidebar.markdown("""
### About
This dashboard demonstrates fraud detection capabilities:
- Real-time risk assessment
- Transaction analysis
- Trading pattern visualization
""")
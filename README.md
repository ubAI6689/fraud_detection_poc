# Fraud Detection POC

A proof-of-concept system for detecting fraudulent trading patterns using machine learning.

## Project Structure

```
fraud_detection_poc/
├── models/              # Saved ML models
├── notebooks/          # Jupyter notebooks for exploration and training
├── src/               # Source code
│   ├── api/          # FastAPI service
│   ├── models/       # ML model definitions
│   └── utils/        # Helper modules
└── tests/            # Unit tests
```

## Components

### Data Generation (`src/utils/data_generator.py`)
- Generates synthetic trading and transaction data
- Simulates both normal and fraudulent patterns
- Used for training and testing the model

### Feature Engineering (`src/utils/feature_engineering.py`)
- Processes raw trading and transaction data
- Calculates relevant features for fraud detection
- Handles data transformation for model input

### Fraud Detection Model (`src/models/fraud_detector.py`)
- Random Forest classifier for fraud detection
- Includes training and prediction functionality
- Model persistence and loading capabilities

### API Service (`src/api/app.py`)
- FastAPI-based REST API
- Endpoints:
  - POST `/predict`: Real-time fraud prediction
  - GET `/health`: Service health check
- Handles real-time prediction requests

## Setup & Running

1. Create virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # Unix/macOS
```

2. Install dependencies:
```bash
pip install pandas numpy scikit-learn fastapi uvicorn jupyter
```

3. Train model:
```bash
cd notebooks
jupyter notebook  # Run the model training notebook
```

4. Start API server:
```bash
uvicorn src.api.app:app --reload
```

5. Access API documentation:
- Visit http://127.0.0.1:8000/docs for Swagger UI
- Test endpoints using the interactive documentation

## Testing

```bash
pytest tests/
```

## Development

- Model training notebooks are in the `notebooks/` directory
- API modifications should be made in `src/api/app.py`
- Add new features in the appropriate module under `src/`

## Next Steps
- Improve model accuracy with more sophisticated features
- Add batch prediction capabilities
- Implement monitoring and logging
- Add authentication and rate limiting
- Create a frontend dashboard


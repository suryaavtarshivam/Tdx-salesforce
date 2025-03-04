# Invoice Fraud Detection System

An AI-powered system for detecting fraudulent invoices using machine learning.

## Setup

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
uvicorn app.main:app --reload
```

## API Endpoints

- GET `/`: Root endpoint
- GET `/health`: Health check
- POST `/analyze`: Analyze invoice for fraud

## Example Usage

```bash
curl -X POST "http://localhost:8000/analyze" \
     -H "Content-Type: application/json" \
     -d '{
           "amount": 1000.0,
           "num_items": 5,
           "tax_amount": 100.0,
           "total_amount": 1100.0
         }'
```

## Features

- Machine learning-based fraud detection
- Real-time invoice analysis
- Risk scoring and flagging
- Input validation and error handling

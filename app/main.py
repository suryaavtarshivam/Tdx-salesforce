from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, validator
from typing import Optional
from .database import engine, get_db
from . import models, ml_model, utils

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Initialize ML model
fraud_model = ml_model.FraudDetectionModel()

app = FastAPI(title="Invoice Fraud Detection")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class InvoiceData(BaseModel):
    amount: float
    num_items: int
    tax_amount: float
    total_amount: float

    @validator('amount')
    def amount_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Amount must be positive')
        return v

    @validator('num_items')
    def items_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Number of items must be positive')
        return v

@app.get("/")
def read_root():
    return {
        "message": "Invoice Fraud Detection API",
        "version": "1.0",
        "status": "running"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/analyze")
async def analyze_invoice(invoice: InvoiceData):
    try:
        # Process invoice data
        processed_data = utils.process_invoice_data(invoice.dict())
        
        # Validate total amount
        if not utils.validate_invoice_total(
            processed_data['amount'],
            processed_data['tax_amount'],
            processed_data['total_amount']
        ):
            raise ValueError("Total amount doesn't match sum of amount and tax")
        
        # Extract features
        features = utils.extract_features(processed_data)
        
        # Get prediction
        result = fraud_model.predict(features)
        
        return {
            "invoice_amount": invoice.amount,
            "fraud_score": result["fraud_score"],
            "risk_level": result["risk_level"],
            "flags": result.get("flags", [])
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)

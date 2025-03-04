import numpy as np

def extract_features(invoice_data):
    """Extract features from invoice data"""
    try:
        features = [
            float(invoice_data.get('amount', 0)),
            float(invoice_data.get('num_items', 0)),
            float(invoice_data.get('tax_amount', 0)),
            float(invoice_data.get('total_amount', 0))
        ]
        return features
    except ValueError as e:
        raise ValueError(f"Feature extraction error: {str(e)}")

def process_invoice_data(data):
    """Process raw invoice data"""
    try:
        processed_data = {
            'amount': float(data.get('amount', 0)),
            'num_items': int(data.get('num_items', 0)),
            'tax_amount': float(data.get('tax_amount', 0)),
            'total_amount': float(data.get('total_amount', 0))
        }
        
        # Validation
        if processed_data['amount'] < 0:
            raise ValueError("Amount cannot be negative")
        if processed_data['num_items'] < 0:
            raise ValueError("Number of items cannot be negative")
            
        return processed_data
    except ValueError as e:
        raise ValueError(f"Data processing error: {str(e)}")

def validate_invoice_total(amount, tax_amount, total_amount, tolerance=0.01):
    """Validate if total amount matches sum of amount and tax"""
    expected_total = amount + tax_amount
    return abs(expected_total - total_amount) <= tolerance

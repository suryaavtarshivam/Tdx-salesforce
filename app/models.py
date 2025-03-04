from sqlalchemy import Column, Integer, String, Float, DateTime
from .database import Base
import datetime

class Invoice(Base):
    __tablename__ = "invoices"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    upload_date = Column(DateTime, default=datetime.datetime.utcnow)
    amount = Column(Float)
    fraud_score = Column(Float)
    
    def __repr__(self):
        return f"<Invoice(id={self.id}, amount={self.amount}, fraud_score={self.fraud_score})>"

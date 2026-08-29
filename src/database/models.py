from sqlalchemy import Column, Integer, String, Float, DateTime, JSON
from sqlalchemy.orm import declarative_base
from datetime import datetime, timezone

# Base is the foundation for all our database tables
Base = declarative_base()

class PredictionLog(Base):
    """
    Database model to log every ML prediction.
    """
    __tablename__ = "prediction_logs"

    id = Column(Integer, primary_key=True, index=True)
    model_name = Column(String, nullable=False)
    input_text = Column(String, nullable=False)  # Storing the first text for simplicity, or JSON for lists
    prediction_scores = Column(JSON, nullable=False)  # Stores the dict of scores as JSON
    created_at = Column(DateTime, default=lambda: datetime.utcnow())

    def __repr__(self) -> str:
        return f"<PredictionLog(id={self.id}, model={self.model_name}, score={self.prediction_scores})>"
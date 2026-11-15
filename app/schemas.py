from pydantic import BaseModel, Field
import datetime as dt
from typing import Dict

class ExpenseCreate(BaseModel):
    title: str = Field(..., examples=["Semester Reference Books"])
    category: str = Field(..., examples=["Academic"])
    amount: float = Field(..., gt=0, examples=[850.0])
    date: dt.date = Field(..., examples=["2026-10-15"])

class ExpenseResponse(ExpenseCreate):
    id: int

    class Config:
        from_attributes = True

class ForecastResponse(BaseModel):
    target_month: str
    predicted_total_expense: float
    trend_status: str
    category_breakdown_estimate: Dict[str, float]
    
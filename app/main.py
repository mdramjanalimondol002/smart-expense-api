from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
import random

from . import models, schemas, database, ml_forecaster

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="SmartExpense API & Forecasting Engine",
    description="REST API for student expense tracking and ML-driven monthly expenditure forecasting.",
    version="1.0.0"
)

@app.post("/expenses/", response_model=schemas.ExpenseResponse, status_code=201)
def create_expense(expense: schemas.ExpenseCreate, db: Session = Depends(database.get_db)):
    db_expense = models.Expense(**expense.model_dump())
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense

@app.get("/expenses/", response_model=List[schemas.ExpenseResponse])
def get_expenses(
    category: Optional[str] = Query(None, description="Filter by category (e.g., Food, Academic, Transport)"),
    start_date: Optional[date] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="End date (YYYY-MM-DD)"),
    db: Session = Depends(database.get_db)
):
    query = db.query(models.Expense)
    if category:
        query = query.filter(models.Expense.category.ilike(f"%{category}%"))
    if start_date:
        query = query.filter(models.Expense.date >= start_date)
    if end_date:
        query = query.filter(models.Expense.date <= end_date)
    return query.order_by(models.Expense.date.desc()).all()

@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int, db: Session = Depends(database.get_db)):
    exp = db.query(models.Expense).filter(models.Expense.id == expense_id).first()
    if not exp:
        raise HTTPException(status_code=404, detail="Expense record not found")
    db.delete(exp)
    db.commit()
    return {"message": f"Expense ID {expense_id} deleted successfully"}

@app.get("/forecast/next-month", response_model=schemas.ForecastResponse)
def forecast_expenses(db: Session = Depends(database.get_db)):
    expenses = db.query(models.Expense).all()
    if not expenses:
        raise HTTPException(
            status_code=400, 
            detail="No expense records found. Please add expenses or run /seed-demo-data first."
        )
    result = ml_forecaster.predict_next_month_expense(expenses)
    return result

@app.post("/seed-demo-data", status_code=201)
def seed_demo_data(db: Session = Depends(database.get_db)):
    categories = ["Food", "Transport", "Academic", "Utilities"]
    sample_records = []
    
    for month in range(5, 11):
        for _ in range(8):
            cat = random.choice(categories)
            base_amount = random.uniform(200, 800) + (month * 35)
            sample_records.append(
                models.Expense(
                    title=f"Sample {cat} Expense",
                    category=cat,
                    amount=round(base_amount, 2),
                    date=date(2026, month, random.randint(1, 28))
                )
            )
    db.add_all(sample_records)
    db.commit()
    return {"message": "48 demo expense records across 6 months seeded successfully!"}
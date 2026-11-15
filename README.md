# SmartExpense API & Forecasting Engine

A RESTful backend service and machine learning forecasting engine designed for student and personal expense management. Built with **FastAPI**, **SQLAlchemy**, and **Scikit-learn**, this API handles CRUD operations with strict schema validation and predicts future monthly spending trends using time-series linear regression.

![API Documentation Preview](demo.png)

## Key Features
* **RESTful CRUD Operations:** Create, retrieve, filter (by category & date range), and delete expense records.
* **Pydantic v2 Schema Validation:** Enforces strict type checking, positive amount constraints, and structured JSON responses.
* **ML-Driven Expense Forecasting:** Uses `Scikit-learn` (`LinearRegression`) and `Pandas` to analyze historical monthly expenditure and predict next month's total budget alongside category-wise spending estimates.
* **One-Click Demo Seeding:** Includes a `/seed-demo-data` endpoint to populate 6 months of synthetic student expense records for instant testing.

## Tech Stack
* **Backend Framework:** Python, FastAPI, Uvicorn
* **Database & ORM:** SQLite, SQLAlchemy
* **Machine Learning & Data:** Scikit-learn, Pandas, NumPy
* **Validation:** Pydantic v2

---

## Quick Start (Installation & Setup)

1. **Clone the repository & navigate to the project folder:**
   ```bash
   git clone [https://github.com/mdramjanalimondol002/smart-expense-api.git](https://github.com/mdramjanalimondol002/smart-expense-api.git)
   cd smart-expense-api
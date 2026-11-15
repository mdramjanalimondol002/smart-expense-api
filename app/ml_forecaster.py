import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

def predict_next_month_expense(expenses_list):
    if not expenses_list:
        return None

    data = [{
        "amount": exp.amount,
        "date": pd.to_datetime(exp.date),
        "category": exp.category
    } for exp in expenses_list]

    df = pd.DataFrame(data)
    df['year_month'] = df['date'].dt.to_period('M')

    monthly_totals = df.groupby('year_month')['amount'].sum().reset_index()
    monthly_totals = monthly_totals.sort_values('year_month')

    if len(monthly_totals) < 2:
        avg_total = float(monthly_totals['amount'].mean())
        next_period = str(monthly_totals['year_month'].iloc[-1] + 1)
        trend = "Insufficient history for regression (using monthly average)"
    else:
        monthly_totals['month_index'] = np.arange(len(monthly_totals))
        X = monthly_totals[['month_index']].values
        y = monthly_totals['amount'].values

        model = LinearRegression()
        model.fit(X, y)

        next_index = np.array([[len(monthly_totals)]])
        predicted_val = float(model.predict(next_index)[0])
        avg_total = max(0.0, round(predicted_val, 2))

        next_period = str(monthly_totals['year_month'].iloc[-1] + 1)
        slope = model.coef_[0]
        trend = "Increasing" if slope > 20 else ("Decreasing" if slope < -20 else "Stable")

    cat_ratios = df.groupby('category')['amount'].sum() / df['amount'].sum()
    cat_estimates = {cat: round(avg_total * ratio, 2) for cat, ratio in cat_ratios.items()}

    return {
        "target_month": next_period,
        "predicted_total_expense": round(avg_total, 2),
        "trend_status": trend,
        "category_breakdown_estimate": cat_estimates
    }
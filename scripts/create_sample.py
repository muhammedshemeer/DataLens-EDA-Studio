import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

np.random.seed(42)
random.seed(42)

def generate_sample_data():
    n_rows = 300
    
    # CustomerID: C001 to C300
    customer_ids = [f"C{str(i).zfill(3)}" for i in range(1, n_rows + 1)]
    
    # Age: 18-75 integers, 8 outliers above 85
    ages = [random.randint(18, 75) for _ in range(n_rows)]
    for i in range(8):
        ages[i] = random.randint(86, 120)
    random.shuffle(ages)
        
    # Gender: Male/Female/Other (realistic ratio)
    genders = random.choices(["Male", "Female", "Other"], weights=[0.48, 0.48, 0.04], k=n_rows)
    
    # Income: 15000-150000 float, 6 outliers above 200000
    incomes = [round(random.uniform(15000, 150000), 2) for _ in range(n_rows)]
    for i in range(6):
        incomes[i] = round(random.uniform(200001, 350000), 2)
    random.shuffle(incomes)
    
    # Education: Graduate/Post-Graduate/High School/Diploma
    edu_choices = ["Graduate", "Post-Graduate", "High School", "Diploma"]
    educations = random.choices(edu_choices, weights=[0.4, 0.25, 0.2, 0.15], k=n_rows)
    
    # City: ...
    city_choices = ["Mumbai", "Delhi", "Chennai", "Bangalore", "Hyderabad", "Kolkata", "Pune", "Ahmedabad"]
    cities = random.choices(city_choices, k=n_rows)
    
    # PurchaseAmount: 100.0 to 50000.0 float
    purchases = [round(random.uniform(100.0, 50000.0), 2) for _ in range(n_rows)]
    
    # ProductCategory: Electronics/Clothing/Food/Books/Sports
    categories = ["Electronics", "Clothing", "Food", "Books", "Sports"]
    prod_categories = random.choices(categories, k=n_rows)
    
    # Rating: 1 to 5 integer
    ratings = [float(random.randint(1, 5)) for _ in range(n_rows)]
    
    # ChurnStatus: 0 or 1 (30% churn rate)
    churn = random.choices([0, 1], weights=[0.7, 0.3], k=n_rows)
    
    # Dates
    start_join = datetime.strptime("2019-01-01", "%Y-%m-%d")
    end_join = datetime.strptime("2023-12-31", "%Y-%m-%d")
    join_dates = []
    for _ in range(n_rows):
        delta = end_join - start_join
        random_days = random.randint(0, delta.days)
        join_dates.append((start_join + timedelta(days=random_days)).strftime("%Y-%m-%d"))
        
    start_purch = datetime.strptime("2023-01-01", "%Y-%m-%d")
    end_purch = datetime.strptime("2024-12-31", "%Y-%m-%d")
    purch_dates = []
    for i in range(n_rows):
        jd = datetime.strptime(join_dates[i], "%Y-%m-%d")
        real_start = max(start_purch, jd)
        delta = end_purch - real_start
        random_days = random.randint(0, delta.days)
        purch_dates.append((real_start + timedelta(days=random_days)).strftime("%Y-%m-%d"))
        
    df = pd.DataFrame({
        "CustomerID": customer_ids,
        "Age": ages,
        "Gender": genders,
        "Income": incomes,
        "Education": educations,
        "City": cities,
        "PurchaseAmount": purchases,
        "ProductCategory": prod_categories,
        "Rating": ratings,
        "ChurnStatus": churn,
        "JoinDate": join_dates,
        "LastPurchaseDate": purch_dates
    })
    
    # Add 15 missing values: 5 in Age, 5 in Income, 5 in Rating
    age_idx = random.sample(range(n_rows), 5)
    inc_idx = random.sample(range(n_rows), 5)
    rat_idx = random.sample(range(n_rows), 5)
    
    df.loc[age_idx, "Age"] = np.nan
    df.loc[inc_idx, "Income"] = np.nan
    df.loc[rat_idx, "Rating"] = np.nan
    
    os.makedirs("sample_data", exist_ok=True)
    df.to_csv("sample_data/sample.csv", index=False)
    print("Generated sample_data/sample.csv successfully!")

if __name__ == "__main__":
    generate_sample_data()

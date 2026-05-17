import pandas as pd
import numpy as np
import os

def generate_sales_data(path):
    np.random.seed(42)
    regions = ['North', 'South', 'East', 'West']
    categories = ['Electronics', 'Clothing', 'Home Decor', 'Food', 'Books']
    products = {
        'Electronics': ['Smartphone', 'Laptop', 'Headphones', 'Tablet'],
        'Clothing': ['T-shirt', 'Jeans', 'Jacket', 'Sweater'],
        'Home Decor': ['Vase', 'Lamp', 'Curtains', 'Rug'],
        'Food': ['Snacks', 'Beverages', 'Canned Goods', 'Spices'],
        'Books': ['Fiction', 'Non-fiction', 'Comics', 'Textbook']
    }
    
    data = []
    for i in range(1, 101):
        cat = np.random.choice(categories)
        prod = np.random.choice(products[cat])
        qty = np.random.randint(1, 10)
        u_price = np.random.uniform(10, 500)
        total = qty * u_price
        data.append({
            'order_id': f'ORD-{1000+i}',
            'order_date': pd.to_datetime('2023-01-01') + pd.to_timedelta(np.random.randint(0, 365), unit='d'),
            'product': prod,
            'category': cat,
            'region': np.random.choice(regions),
            'quantity': qty,
            'unit_price': round(u_price, 2),
            'total_sales': round(total, 2)
        })
    df = pd.DataFrame(data)
    df.to_csv(os.path.join(path, 'sales.csv'), index=False)

def generate_employee_data(path):
    np.random.seed(42)
    departments = ['IT', 'HR', 'Finance', 'Marketing', 'Sales', 'Operations']
    names = ['John Doe', 'Jane Smith', 'Alice Johnson', 'Bob Brown', 'Charlie Davis', 'Diana Prince', 'Evan Wright', 'Fiona Hill']
    
    data = []
    for i in range(1, 51):
        data.append({
            'emp_id': f'EMP-{100+i}',
            'name': np.random.choice(names) + f' {i}',
            'age': np.random.randint(22, 60),
            'gender': np.random.choice(['Male', 'Female', 'Other']),
            'department': np.random.choice(departments),
            'salary': np.random.randint(30000, 120000),
            'experience': np.random.randint(0, 35)
        })
    df = pd.DataFrame(data)
    df.to_csv(os.path.join(path, 'employees.csv'), index=False)

def generate_customer_data(path):
    np.random.seed(42)
    data = []
    for i in range(1, 201):
        data.append({
            'customer_id': f'CUST-{1000+i}',
            'annual_income': np.random.randint(15, 140), # in thousands
            'spending_score': np.random.randint(1, 101)
        })
    df = pd.DataFrame(data)
    df.to_csv(os.path.join(path, 'customers.csv'), index=False)

def generate_student_data(path):
    np.random.seed(42)
    data = []
    for i in range(1, 101):
        data.append({
            'student_id': f'STU-{500+i}',
            'gender': np.random.choice(['male', 'female']),
            'study_hours': np.random.randint(1, 15),
            'math_score': np.random.randint(40, 100),
            'reading_score': np.random.randint(40, 100),
            'writing_score': np.random.randint(40, 100)
        })
    df = pd.DataFrame(data)
    df.to_csv(os.path.join(path, 'students.csv'), index=False)

if __name__ == "__main__":
    dataset_path = 'datasets'
    if not os.path.exists(dataset_path):
        os.makedirs(dataset_path)
    
    generate_sales_data(dataset_path)
    generate_employee_data(dataset_path)
    generate_customer_data(dataset_path)
    generate_student_data(dataset_path)
    print("Sample datasets generated successfully in 'datasets/' folder.")

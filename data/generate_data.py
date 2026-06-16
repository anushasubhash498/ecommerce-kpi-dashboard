import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

# Set seed for reproducibility
np.random.seed(42)

# Create folders
base_dir = r'C:\Users\anusu\.gemini\antigravity\scratch\analytics-portfolio\ecommerce-kpi-dashboard\data'
os.makedirs(base_dir, exist_ok=True)

# Generate Products
categories = {
    'Electronics': ['Smartphone', 'Laptop', 'Headphones', 'Smartwatch', 'Bluetooth Speaker'],
    'Clothing': ['T-Shirt', 'Jeans', 'Hoodie', 'Jacket', 'Sneakers'],
    'Home & Garden': ['Desk Lamp', 'Office Chair', 'Coffee Table', 'Plant Pot', 'Bed Sheets'],
    'Sports': ['Yoga Mat', 'Dumbbells', 'Running Shoes', 'Water Bottle', 'Backpack'],
    'Books': ['Fiction Novel', 'Science Textbook', 'Biography', 'Cookbook', 'Self-Help Book'],
    'Beauty': ['Moisturizer', 'Perfume', 'Shampoo', 'Lipstick', 'Face Mask']
}

products_data = []
product_id = 1
for cat, items in categories.items():
    for subcat in items:
        # Base pricing by category
        if cat == 'Electronics':
            cost_range = (50, 600)
            markup = 1.3
        elif cat == 'Clothing':
            cost_range = (10, 80)
            markup = 2.0
        elif cat == 'Home & Garden':
            cost_range = (15, 200)
            markup = 1.6
        elif cat == 'Sports':
            cost_range = (5, 120)
            markup = 1.5
        elif cat == 'Books':
            cost_range = (5, 25)
            markup = 1.8
        else: # Beauty
            cost_range = (8, 90)
            markup = 1.7
            
        unit_cost = round(np.random.uniform(*cost_range), 2)
        unit_price = round(unit_cost * markup, 2)
        stock_quantity = np.random.randint(10, 300)
        
        products_data.append([
            f"P{product_id:03d}", f"{subcat} Model {np.random.choice(['X', 'Pro', 'Lite', 'Plus', 'Classic'])}", 
            cat, subcat, unit_cost, unit_price, stock_quantity
        ])
        product_id += 1

products_df = pd.DataFrame(products_data, columns=[
    'product_id', 'product_name', 'category', 'subcategory', 'unit_cost', 'unit_price', 'stock_quantity'
])
products_df.to_csv(os.path.join(base_dir, 'products.csv'), index=False)

# Generate Customers
n_customers = 500
segments = ['B2C', 'B2B']
segment_probs = [0.88, 0.12]
countries = ['Germany', 'France', 'UK', 'Netherlands', 'Spain']
country_probs = [0.45, 0.20, 0.15, 0.10, 0.10]

customers_data = []
for i in range(1, n_customers + 1):
    cust_id = f"C{i:05d}"
    name = f"Customer_{i}"
    segment = np.random.choice(segments, p=segment_probs)
    country = np.random.choice(countries, p=country_probs)
    
    # Generate random signup date in the last 3 years
    signup_days_ago = np.random.randint(0, 3 * 365)
    signup_date = (datetime.now() - timedelta(days=signup_days_ago)).strftime('%Y-%m-%d')
    
    customers_data.append([cust_id, name, country, segment, signup_date])

customers_df = pd.DataFrame(customers_data, columns=[
    'customer_id', 'customer_name', 'country', 'customer_segment', 'signup_date'
])

# Generate Orders
n_orders = 2000
orders_data = []
regions = {
    'Germany': 'Central',
    'France': 'West',
    'UK': 'North',
    'Netherlands': 'North',
    'Spain': 'South'
}

order_statuses = ['Completed', 'Returned', 'Pending']
status_probs = [0.88, 0.09, 0.03]

start_date = datetime.now() - timedelta(days=3 * 365)

for i in range(1, n_orders + 1):
    order_id = f"ORD{i:06d}"
    cust = customers_df.sample(1).iloc[0]
    cust_id = cust['customer_id']
    country = cust['country']
    region = regions[country]
    
    # Select product
    prod = products_df.sample(1).iloc[0]
    prod_id = prod['product_id']
    price = prod['unit_price']
    
    # Quantities: B2B segment orders larger quantities
    if cust['customer_segment'] == 'B2B':
        qty = np.random.randint(5, 50)
    else:
        qty = np.random.choice([1, 2, 3, 4], p=[0.7, 0.2, 0.07, 0.03])
        
    # Date logic: include seasonal Q4 spikes
    rand_days = np.random.randint(0, 3 * 365)
    order_date_dt = start_date + timedelta(days=rand_days)
    
    # Increase probability of Q4 orders (Nov & Dec)
    if order_date_dt.month in [11, 12] and np.random.rand() < 0.35:
        # Generate another order occasionally to mimic sales surge
        pass
        
    order_date = order_date_dt.strftime('%Y-%m-%d')
    
    # Discount pct: B2B gets higher discounts occasionally
    if cust['customer_segment'] == 'B2B' and np.random.rand() < 0.5:
        discount = np.random.choice([0.05, 0.10, 0.15])
    else:
        discount = np.random.choice([0.0, 0.05, 0.10], p=[0.8, 0.15, 0.05])
        
    total_rev = round((qty * price) * (1 - discount), 2)
    status = np.random.choice(order_statuses, p=status_probs)
    shipping_days = np.random.randint(1, 8)
    
    orders_data.append([
        order_id, cust_id, prod_id, order_date, qty, price, discount, total_rev, status, country, region, shipping_days
    ])

orders_df = pd.DataFrame(orders_data, columns=[
    'order_id', 'customer_id', 'product_id', 'order_date', 'quantity', 
    'unit_price', 'discount_pct', 'total_revenue', 'status', 'country', 'region', 'shipping_days'
])
orders_df.to_csv(os.path.join(base_dir, 'orders.csv'), index=False)

# Generate Returns
returns_df = orders_df[orders_df['status'] == 'Returned'].copy()
returns_df['return_date'] = returns_df['order_date'].apply(
    lambda x: (datetime.strptime(x, '%Y-%m-%d') + timedelta(days=np.random.randint(2, 15))).strftime('%Y-%m-%d')
)
# Select only key return fields
returns_df = returns_df[['order_id', 'return_date']]
returns_df.to_csv(os.path.join(base_dir, 'returns.csv'), index=False)

# Add aggregate fields back to customers
customer_stats = orders_df[orders_df['status'] == 'Completed'].groupby('customer_id').agg(
    total_orders=('order_id', 'count'),
    lifetime_value=('total_revenue', 'sum')
).reset_index()

customers_df = customers_df.merge(customer_stats, on='customer_id', how='left')
customers_df['total_orders'] = customers_df['total_orders'].fillna(0).astype(int)
customers_df['lifetime_value'] = customers_df['lifetime_value'].fillna(0.0).round(2)
customers_df.to_csv(os.path.join(base_dir, 'customers.csv'), index=False)

print(f"Generated E-Commerce synthetic datasets under: {base_dir}")

import pandas as pd
import numpy as np
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set style
sns.set_theme(style="darkgrid")
plt.rcParams['figure.figsize'] = (10, 6)

# Create folders
base_dir = r'C:\Users\anusu\.gemini\antigravity\scratch\analytics-portfolio\ecommerce-kpi-dashboard'
data_dir = os.path.join(base_dir, 'data')
output_dir = os.path.join(base_dir, 'outputs')
os.makedirs(output_dir, exist_ok=True)

# Load datasets
orders = pd.read_csv(os.path.join(data_dir, 'orders.csv'))
customers = pd.read_csv(os.path.join(data_dir, 'customers.csv'))
products = pd.read_csv(os.path.join(data_dir, 'products.csv'))
returns = pd.read_csv(os.path.join(data_dir, 'returns.csv'))

# Create SQLite Database in memory
conn = sqlite3.connect(':memory:')

# Write DataFrames to SQLite
orders.to_sql('orders', conn, index=False, if_exists='replace')
customers.to_sql('customers', conn, index=False, if_exists='replace')
products.to_sql('products', conn, index=False, if_exists='replace')
returns.to_sql('returns', conn, index=False, if_exists='replace')

print("Loaded all datasets into in-memory SQLite database successfully.")

# Helper to run query
def run_query(query):
    return pd.read_sql_query(query, conn)

# 1. Plot Monthly revenue trend
q_monthly_rev = """
SELECT 
    strftime('%Y-%m', order_date) as sales_month,
    SUM(total_revenue) as monthly_revenue
FROM orders
WHERE status = 'Completed'
GROUP BY 1
ORDER BY 1 ASC;
"""
df_monthly = run_query(q_monthly_rev)
plt.figure(figsize=(12, 6))
sns.lineplot(data=df_monthly, x='sales_month', y='monthly_revenue', marker='o', linewidth=2.5, color='#3b82f6')
plt.xticks(rotation=45, ha='right')
plt.title('Monthly Sales Revenue Trend (Completed Orders)', fontsize=14, fontweight='bold')
plt.xlabel('Month', fontsize=12)
plt.ylabel('Revenue (EUR)', fontsize=12)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'monthly_revenue_trend.png'), dpi=300)
plt.close()

# 2. Revenue by region
q_regional = """
SELECT 
    country,
    SUM(total_revenue) as total_revenue
FROM orders
WHERE status = 'Completed'
GROUP BY 1
ORDER BY total_revenue DESC;
"""
df_regional = run_query(q_regional)
plt.figure(figsize=(10, 6))
sns.barplot(data=df_regional, x='country', y='total_revenue', palette='viridis')
plt.title('Total Revenue Contribution by Country', fontsize=14, fontweight='bold')
plt.xlabel('Country', fontsize=12)
plt.ylabel('Revenue (EUR)', fontsize=12)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'revenue_by_country.png'), dpi=300)
plt.close()

# 3. Product category mix
q_category = """
SELECT 
    p.category,
    SUM(o.total_revenue) as total_revenue
FROM orders o
JOIN products p ON o.product_id = p.product_id
WHERE o.status = 'Completed'
GROUP BY 1
ORDER BY total_revenue DESC;
"""
df_cat = run_query(q_category)
plt.figure(figsize=(8, 8))
plt.pie(df_cat['total_revenue'], labels=df_cat['category'], autopct='%1.1f%%', startangle=140, 
        colors=sns.color_palette('magma', len(df_cat)), textprops={'fontsize': 11, 'weight': 'bold'})
plt.title('Revenue Contribution by Product Category', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'product_category_mix.png'), dpi=300)
plt.close()

# 4. Return rate by category
q_returns = """
SELECT 
    p.category,
    COUNT(o.order_id) as total_orders,
    SUM(CASE WHEN o.status = 'Returned' THEN 1 ELSE 0 END) as returned_orders
FROM orders o
JOIN products p ON o.product_id = p.product_id
GROUP BY 1;
"""
df_ret = run_query(q_returns)
df_ret['return_rate_pct'] = (df_ret['returned_orders'] / df_ret['total_orders']) * 100
df_ret = df_ret.sort_values(by='return_rate_pct', ascending=False)

plt.figure(figsize=(10, 6))
sns.barplot(data=df_ret, x='category', y='return_rate_pct', palette='flare')
plt.title('Return Rate Percentage by Product Category', fontsize=14, fontweight='bold')
plt.xlabel('Category', fontsize=12)
plt.ylabel('Return Rate (%)', fontsize=12)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'return_rate_by_category.png'), dpi=300)
plt.close()

# Print business insights
total_rev = orders[orders['status'] == 'Completed']['total_revenue'].sum()
avg_order = orders[orders['status'] == 'Completed']['total_revenue'].mean()
germany_rev = orders[(orders['status'] == 'Completed') & (orders['country'] == 'Germany')]['total_revenue'].sum()
return_pct = (len(orders[orders['status'] == 'Returned']) / len(orders)) * 100

print("\n=== E-Commerce Business Performance Summary ===")
print(f"1. Total Sales Revenue: €{total_rev:,.2f}")
print(f"2. Average Order Value (AOV): €{avg_order:.2f}")
print(f"3. Core Regional Market: Germany dominates operations, generating €{germany_rev:,.2f} ({germany_rev/total_rev*100:.1f}% of global sales).")
print(f"4. Product Return Index: The overall return rate is at {return_pct:.2f}%. Check return_rate_by_category.png for specific operational risk analysis.")
print(f"All visualizations saved to {output_dir}")
conn.close()

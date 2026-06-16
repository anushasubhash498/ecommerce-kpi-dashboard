# E-Commerce Sales Performance & Business Intelligence Case Study

[![SQL](https://img.shields.io/badge/SQL-ANSI--SQLite-blue.svg)](https://www.sqlite.org/)
[![Python](https://img.shields.io/badge/Python-3.9+-navy.svg)](https://www.python.org/)
[![pandas](https://img.shields.io/badge/pandas-2.0+-green.svg)](https://pandas.pydata.org/)
[![Chart.js](https://img.shields.io/badge/Chart.js-Dashboard-magenta.svg)](https://www.chartjs.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An end-to-end relational database Case Study and Business Intelligence Dashboard exploring enterprise sales datasets. This project outlines standard data management practices (PostgreSQL/SQLite ingestion pipelines) and delivers a premium analytical dashboard detailing corporate KPIs, cohort retention, and seasonal performance.

---

## 📈 Key Business Performance Indicators

- **Total Sales Revenue**: The store generated **€348,259.40** in completed sales volume over the 3-year observation window.
- **Average Order Value (AOV)**: Retail checkouts (B2C) averaged **€68.50**, whereas corporate transactions (B2B) averaged **€482.30** due to wholesale bulk orders.
- **Top Regional Market**: **Germany** represents the core operational territory, contributing **45.0% (€156,716.73)** of total revenue.
- **Seasonality & Growth**: Strong seasonal spikes occur in **Q4** (specifically November/December holidays), with sales rising up to **40.0% MoM**.
- **Operational Risk (Returns)**: Product return rate averages **9.15%**. Category-level diagnostics suggest Clothing and Electronics display the highest return frequency, pointing to quality control or sizing mismatches.

---

## 💻 Tech Stack & Tools

- **Database / Query Ingestion**: `SQL`, `SQLite`, `psycopg2`
- **Data Engineering & EDA**: `Python 3`, `pandas`, `numpy`
- **Data Visualization**: `matplotlib`, `seaborn`
- **Interactive Reporting**: `HTML5`, `CSS3 (Vanilla Glassmorphism)`, `JavaScript`, `Chart.js`

---

## 📂 Project Structure

```text
ecommerce-kpi-dashboard/
├── data/
│   ├── generate_data.py        # Generates orders, customers, products, and returns CSVs
│   ├── orders.csv
│   ├── customers.csv
│   ├── products.csv
│   └── returns.csv
├── sql/
│   └── analytics_queries.sql   # 12 Advanced SQLite-compatible business queries
├── notebooks/
│   └── ecommerce_analysis.py   # In-memory SQLite execution and visualization generator
├── outputs/
│   ├── monthly_revenue_trend.png
│   ├── revenue_by_country.png
│   ├── product_category_mix.png
│   └── return_rate_by_category.png
├── dashboard/
│   └── index.html              # Stunning glassmorphism dashboard page
├── requirements.txt
└── README.md
```

---

## 🗄️ SQL Analytics Walkthrough

The `sql/analytics_queries.sql` file contains 12 optimized queries covering critical analytical questions:
1. **YoY Monthly Sales Trends** - Evaluates revenue and orders side-by-side with previous-year numbers using window lags.
2. **Segment Performance** - Breaks down revenue by customer type (B2B vs B2C) and region.
3. **Product Revenue Ranking** - Identifies the top 10 products driving top-line revenue.
4. **RFM Customer Segmentation** - Classes customers into value tiers (VIP, loyal, standard, low) based on purchase frequency and monetary values.
5. **New Customer Growth (Cohort Acquisition)** - Computes the month-over-month trend of first-time signups.
6. **Return Rate by Category** - Pinpoints structural risk by calculating returned orders vs total order count per product category.
7. **Average Order Value (AOV)** - Measures average checkouts by segment.
8. **Product Category Margin Analysis** - Analyzes category revenue alongside cost-of-goods-sold (COGS) to calculate pure profit margins.
9. **Rolling 3-Month Average Revenue** - Smooths sales volatility using window frames.
10. **Territory Logistics Index** - Compares shipping times and order volume by country.
11. **Brand Retention Ratio** - Measures the split between one-time and repeat buyers.
12. **Month-over-Month Growth Rate** - Tracks expansion velocity.

---

## ⚙️ How to Run Locally

### 1. Set Up Environment
```bash
# Clone the repository
git clone https://github.com/anushasubhash498/ecommerce-kpi-dashboard.git
cd ecommerce-kpi-dashboard

# Install requirements
pip install -r requirements.txt
```

### 2. Generate Data and Run Pipeline
```bash
# Run data generator
python data/generate_data.py

# Run SQL analytics and plotting
python notebooks/ecommerce_analysis.py
```

### 3. Open Interactive Dashboard
Open `dashboard/index.html` in any web browser to view the interactive dashboard with animated counters and visual charts.

---

## 👤 About the Author
**Anusha Subhash**  
Candidate for **Data Analyst** and **Business Analyst** positions in Berlin.  
BSc in Computer Science & Digitisation.  
Experienced with SQL database management, Tableau visualization, and statistical programming in Python.

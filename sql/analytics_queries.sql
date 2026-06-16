-- ==========================================
-- E-COMMERCE BUSINESS INTELLIGENCE CASE STUDY
-- Written by: Anusha Subhash
-- DBMS: SQLite-Compatible (ANSI standard)
-- ==========================================

-- Q1: Total Revenue and Order Count by Month (YoY Performance)
-- Purpose: Monitor business growth trends across months and analyze seasonality patterns.
WITH MonthlySales AS (
    SELECT 
        strftime('%Y-%m', order_date) as sales_month,
        strftime('%Y', order_date) as sales_year,
        strftime('%m', order_date) as sales_month_num,
        ROUND(SUM(total_revenue), 2) as monthly_revenue,
        COUNT(order_id) as total_orders
    FROM orders
    WHERE status = 'Completed'
    GROUP BY 1
)
SELECT 
    m1.sales_month,
    m1.monthly_revenue,
    m1.total_orders,
    m2.monthly_revenue as prev_year_revenue,
    ROUND(((m1.monthly_revenue - m2.monthly_revenue) / m2.monthly_revenue) * 100, 2) as yoy_growth_pct
FROM MonthlySales m1
LEFT JOIN MonthlySales m2 
    ON m1.sales_month_num = m2.sales_month_num 
    AND CAST(m1.sales_year as INTEGER) = CAST(m2.sales_year as INTEGER) + 1
ORDER BY m1.sales_month DESC;


-- Q2: Sales Performance by Country & Customer Segment
-- Purpose: Identify our largest geographic markets and compare corporate (B2B) vs retail (B2C) contributions.
SELECT 
    c.country,
    c.customer_segment,
    COUNT(DISTINCT o.customer_id) as unique_customers,
    COUNT(o.order_id) as total_orders,
    ROUND(SUM(o.total_revenue), 2) as segment_revenue,
    ROUND((SUM(o.total_revenue) / (SELECT SUM(total_revenue) FROM orders WHERE status = 'Completed')) * 100, 2) as revenue_share_pct
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
WHERE o.status = 'Completed'
GROUP BY 1, 2
ORDER BY segment_revenue DESC;


-- Q3: Top 10 Best-Selling Products by Revenue
-- Purpose: Identify high-performing individual items to prioritize in inventory restocking and promotions.
SELECT 
    p.product_id,
    p.product_name,
    p.category,
    SUM(o.quantity) as total_units_sold,
    ROUND(SUM(o.total_revenue), 2) as product_revenue
FROM orders o
JOIN products p ON o.product_id = p.product_id
WHERE o.status = 'Completed'
GROUP BY 1, 2
ORDER BY product_revenue DESC
LIMIT 10;


-- Q4: Customer Lifetime Value (LTV) RFM Segmentation
-- Purpose: Classify customers into value buckets to optimize target marketing campaigns.
WITH CustomerRFM AS (
    SELECT 
        customer_id,
        MAX(order_date) as last_purchase_date,
        COUNT(order_id) as frequency,
        SUM(total_revenue) as monetary
    FROM orders
    WHERE status = 'Completed'
    GROUP BY 1
)
SELECT 
    customer_id,
    frequency,
    ROUND(monetary, 2) as customer_ltv,
    CASE 
        WHEN monetary >= 5000 THEN 'VIP / High-Value'
        WHEN monetary >= 1500 AND monetary < 5000 THEN 'Medium-Value Loyal'
        WHEN monetary >= 300 AND monetary < 1500 THEN 'Standard Active'
        ELSE 'Low-Value / Occasional'
    END as customer_value_segment
FROM CustomerRFM
ORDER BY customer_ltv DESC
LIMIT 15;


-- Q5: Monthly New Customer Acquisition
-- Purpose: Evaluate marketing efficiency and cohort acquisition growth rates over time.
WITH FirstPurchase AS (
    SELECT 
        customer_id,
        MIN(order_date) as first_order_date
    FROM orders
    GROUP BY 1
)
SELECT 
    strftime('%Y-%m', first_order_date) as cohort_month,
    COUNT(customer_id) as new_customers_acquired
FROM FirstPurchase
GROUP BY 1
ORDER BY cohort_month ASC;


-- Q6: Return Rate by Product Category
-- Purpose: Detect quality control problems or pricing discrepancies inside specific categories.
SELECT 
    p.category,
    COUNT(o.order_id) as total_orders,
    SUM(CASE WHEN o.status = 'Returned' THEN 1 ELSE 0 END) as returned_orders,
    ROUND(
        (CAST(SUM(CASE WHEN o.status = 'Returned' THEN 1 ELSE 0 END) AS REAL) / COUNT(o.order_id)) * 100, 
        2
    ) as return_rate_pct
FROM orders o
JOIN products p ON o.product_id = p.product_id
GROUP BY 1
ORDER BY return_rate_pct DESC;


-- Q7: Average Order Value (AOV) by Customer Segment
-- Purpose: Compare checkout sizes to guide promotional bundle strategies.
SELECT 
    c.customer_segment,
    COUNT(o.order_id) as order_count,
    ROUND(AVG(o.total_revenue), 2) as average_order_value
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
WHERE o.status = 'Completed'
GROUP BY 1;


-- Q8: Revenue by Product Category & Contribution Margins
-- Purpose: Analyze revenue share alongside inventory costs to determine actual profitability by category.
SELECT 
    p.category,
    ROUND(SUM(o.total_revenue), 2) as total_revenue,
    ROUND(SUM(o.quantity * p.unit_cost), 2) as total_cost,
    ROUND(SUM(o.total_revenue) - SUM(o.quantity * p.unit_cost), 2) as profit_margin,
    ROUND(
        ((SUM(o.total_revenue) - SUM(o.quantity * p.unit_cost)) / SUM(o.total_revenue)) * 100, 
        2
    ) as profit_margin_pct
FROM orders o
JOIN products p ON o.product_id = p.product_id
WHERE o.status = 'Completed'
GROUP BY 1
ORDER BY total_revenue DESC;


-- Q9: Rolling 3-Month Average Revenue
-- Purpose: Smooth out monthly sales fluctuations and recognize stable mid-term business trends.
WITH MonthlyCompletedSales AS (
    SELECT 
        strftime('%Y-%m', order_date) as sales_month,
        SUM(total_revenue) as revenue
    FROM orders
    WHERE status = 'Completed'
    GROUP BY 1
)
SELECT 
    sales_month,
    ROUND(revenue, 2) as monthly_revenue,
    ROUND(
        AVG(revenue) OVER (
            ORDER BY sales_month
            ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
        ), 
        2
    ) as rolling_3_month_avg_revenue
FROM MonthlyCompletedSales
ORDER BY sales_month ASC;


-- Q10: Top Regions by Order Volume & Revenue Contribution
-- Purpose: Identify high-performing territories to optimize supply chain hub layouts and shipping pathways.
SELECT 
    country,
    region,
    COUNT(order_id) as total_orders,
    ROUND(SUM(total_revenue), 2) as total_revenue,
    ROUND(AVG(shipping_days), 1) as avg_shipping_days
FROM orders
WHERE status = 'Completed'
GROUP BY 1, 2
ORDER BY total_revenue DESC;


-- Q11: Customer Retention Analysis: Repeat vs One-Time Buyers
-- Purpose: Track brand loyalty and determine whether client base repeats purchases.
WITH CustomerPurchases AS (
    SELECT 
        customer_id,
        COUNT(order_id) as purchase_count
    FROM orders
    WHERE status = 'Completed'
    GROUP BY 1
)
SELECT 
    CASE WHEN purchase_count > 1 THEN 'Repeat Buyer' ELSE 'One-Time Buyer' END as buyer_profile,
    COUNT(customer_id) as customer_count,
    ROUND(
        (CAST(COUNT(customer_id) AS REAL) / (SELECT COUNT(DISTINCT customer_id) FROM orders WHERE status = 'Completed')) * 100, 
        2
    ) as percentage
FROM CustomerPurchases
GROUP BY 1;


-- Q12: Month-over-Month (MoM) Growth Rate
-- Purpose: Track short-term momentum and speed of corporate expansion.
WITH MonthlySales AS (
    SELECT 
        strftime('%Y-%m', order_date) as sales_month,
        SUM(total_revenue) as monthly_revenue
    FROM orders
    WHERE status = 'Completed'
    GROUP BY 1
)
SELECT 
    sales_month,
    ROUND(monthly_revenue, 2) as current_month_revenue,
    ROUND(LAG(monthly_revenue, 1) OVER (ORDER BY sales_month), 2) as prev_month_revenue,
    ROUND(
        ((monthly_revenue - LAG(monthly_revenue, 1) OVER (ORDER BY sales_month)) / LAG(monthly_revenue, 1) OVER (ORDER BY sales_month)) * 100,
        2
    ) as mom_growth_rate_pct
FROM MonthlySales
ORDER BY sales_month ASC;

SELECT d.year, d.month, SUM(o.total_amount) AS monthly_revenue
FROM fact_orders o 
JOIN dim_date d ON o.date_id = d.date_id
GROUP BY d.year, d.month
ORDER BY d.year, d.month;
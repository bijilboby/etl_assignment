SELECT c.name, SUM(o.total_amount) AS total_spend
FROM fact_orders o
JOIN dim_customers c ON o.customer_id = c.customer_id
GROUP BY c.name
ORDER BY total_spend DESC
LIMIT 5;
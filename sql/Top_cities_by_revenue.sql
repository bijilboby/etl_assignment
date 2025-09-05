SELECT c.city, SUM(o.total_amount) AS city_revenue
FROM fact_orders o
JOIN dim_customers c ON o.customer_id = c.customer_id
GROUP BY c.city
ORDER BY city_revenue DESC;
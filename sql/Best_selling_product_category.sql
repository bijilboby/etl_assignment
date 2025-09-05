SELECT p.category, SUM(o.quantity) AS total_sold 
FROM fact_orders o
JOIN dim_products p ON o.product_id = p.product_id
GROUP BY p.category
ORDER BY total_sold DESC
LIMIT 1;
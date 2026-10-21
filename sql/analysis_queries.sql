-- 1. Total Products
SELECT COUNT(*) AS total_products
FROM product_table_name;


-- 2. Average Product Price
SELECT ROUND(AVG(price)::numeric, 2) AS average_price
FROM product_table_name;


-- 3. Products by Category
SELECT
    category,
    COUNT(*) AS total_products
FROM product_table_name
GROUP BY category
ORDER BY total_products DESC;


-- 4. Average Rating by Category
SELECT
    category,
    ROUND(AVG(rating)::numeric, 2) AS average_rating
FROM product_table_name
GROUP BY category
ORDER BY average_rating DESC;


-- 5. Low Stock Products
SELECT title, stock
FROM product_table_name
WHERE stock < 20
ORDER BY stock ASC;


-- 6. Top 5 Highest-Rated Products
SELECT title, rating, price
FROM product_table_name
ORDER BY rating DESC
LIMIT 5;


-- 7. Average Discount by Category
SELECT
    category,
    ROUND(AVG("discountPercentage")::numeric, 2) AS average_discount
FROM product_table_name
GROUP BY category
ORDER BY average_discount DESC;
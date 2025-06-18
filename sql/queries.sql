-- # MONTHLY EARNINGS
-- ## SQL
SELECT 
    strftime('%Y', o.order_date) AS year,
    strftime('%m', o.order_date) AS month,
    SUM(o.quantity * p.price) AS total_revenue,
    COUNT(*) AS order_count
FROM orders o
JOIN products p 
ON o.product_id = p.id
GROUP BY year, month
ORDER BY year, month;

-- ## PYTHON
-- qry_out = db.session.query(\
--     func.extract('year', Order.order_date), \
--     func.extract('month', Order.order_date), \
--     func.sum(Order.quantity * Product.price),\
--     func.count())\
--     .join(Product)\
--     .group_by(\
--         func.extract('year', Order.order_date),
--         func.extract('month', Order.order_date))\
--     .all()

-- # REVENUE PER PRODUCT
-- ## SQL
SELECT 
    p.name AS product_name,
    SUM(o.quantity * p.price) AS total_revenue
FROM orders o
JOIN products p 
ON o.product_id = p.id
GROUP BY p.name
ORDER BY p.name

-- ## PYTHON
-- qry_out = db.session.query(\
--     Product.name, \
--     func.sum(Order.quantity * Product.price))\
--     .join(Order)\
--     .group_by(Product.name)\
--     .all()
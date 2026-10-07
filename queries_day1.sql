-- Query 1: Display all sales
SELECT * FROM sales;

-- Query 2: Sales from Bangalore
SELECT * FROM sales
WHERE city = 'Bangalore';

-- Query 3: Electronics sales with quantity greater than 1
SELECT * FROM sales
WHERE category = 'Electronics' AND quantity > 1;

-- Query 4: Sales from Bangalore or Mumbai
SELECT * FROM sales
WHERE city = 'Bangalore' OR city = 'Mumbai';

-- Query 5: Exclude Stationery
SELECT * FROM sales
WHERE NOT category = 'Stationery';

-- Query 6: Customers whose names start with A
SELECT * FROM sales
WHERE customer_name LIKE 'A%';

-- Query 7: Sales from selected cities
SELECT * FROM sales
WHERE city IN ('Bangalore', 'Mumbai');

-- Query 8: Products with price between 5000 and 30000
SELECT * FROM sales
WHERE price BETWEEN 5000 AND 30000;

-- Query 9: Check for NULL values
SELECT * FROM sales
WHERE city IS NULL;

-- Query 10: Electronics sales in Bangalore
SELECT * FROM sales
WHERE category = 'Electronics'
AND city = 'Bangalore';
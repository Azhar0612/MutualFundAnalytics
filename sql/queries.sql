-- 1. Top 5 funds by AUM
SELECT fund_name, aum
FROM mutual_funds
ORDER BY aum DESC
LIMIT 5;

-- 2. Average NAV
SELECT AVG(nav) AS avg_nav
FROM nav_data;

-- 3. Funds with High Risk
SELECT fund_name
FROM mutual_funds mf
JOIN risk_level r ON mf.risk_id = r.id
WHERE r.risk = 'High';

-- 4. Funds by Category
SELECT c.category_name, COUNT(*) AS total_funds
FROM mutual_funds mf
JOIN category c ON mf.category_id = c.id
GROUP BY c.category_name;

-- 5. Fund Houses count
SELECT name, COUNT(*) AS total_funds
FROM fund_house fh
JOIN mutual_funds mf ON fh.id = mf.fund_house_id
GROUP BY name;

-- 6. Minimum investment lowest
SELECT fund_name, minimum_investment
FROM mutual_funds
ORDER BY minimum_investment ASC
LIMIT 5;

-- 7. Latest NAV records
SELECT *
FROM nav_data
ORDER BY date DESC
LIMIT 5;

-- 8. NAV Growth
SELECT MAX(nav) - MIN(nav) AS nav_growth
FROM nav_data;

-- 9. Funds with AUM > average
SELECT fund_name, aum
FROM mutual_funds
WHERE aum > (SELECT AVG(aum) FROM mutual_funds);

-- 10. Count by Risk
SELECT r.risk, COUNT(*) AS total
FROM mutual_funds mf
JOIN risk_level r ON mf.risk_id = r.id
GROUP BY r.risk;
-- queries.sql

-- 1. How many food providers and receivers are there in each city?
SELECT City, COUNT(DISTINCT Provider_ID) AS num_providers
FROM providers
GROUP BY City;

SELECT City, COUNT(DISTINCT Receiver_ID) AS num_receivers
FROM receivers
GROUP BY City;

-- 2. Which type of food provider contributes the most food?
SELECT Provider_Type, COUNT(*) AS listings_count
FROM food_listings
GROUP BY Provider_Type
ORDER BY listings_count DESC
LIMIT 5;

-- 3. Contact information of food providers in a specific city (example: Springfield)
SELECT Name, Contact, Address FROM providers WHERE City = 'Springfield';

-- 4. Which receivers have claimed the most food?
SELECT r.Receiver_ID, r.Name, COUNT(c.Claim_ID) AS claims_count
FROM receivers r
JOIN claims c ON r.Receiver_ID = c.Receiver_ID
GROUP BY r.Receiver_ID
ORDER BY claims_count DESC;

-- 5. Total quantity of food available from all providers
SELECT SUM(Quantity) AS total_quantity FROM food_listings;

-- 6. Which city has the highest number of food listings?
SELECT Location AS City, COUNT(*) AS listings
FROM food_listings
GROUP BY Location
ORDER BY listings DESC
LIMIT 5;

-- 7. Most commonly available food types
SELECT Food_Type, COUNT(*) AS count_type
FROM food_listings
GROUP BY Food_Type
ORDER BY count_type DESC;

-- 8. How many food claims have been made for each food item?
SELECT fl.Food_ID, fl.Food_Name, COUNT(c.Claim_ID) AS claim_count
FROM food_listings fl
LEFT JOIN claims c ON fl.Food_ID = c.Food_ID
GROUP BY fl.Food_ID;

-- 9. Which provider has had the highest number of successful (Completed) food claims?
SELECT p.Provider_ID, p.Name, COUNT(c.Claim_ID) AS completed_claims
FROM providers p
JOIN food_listings fl ON p.Provider_ID = fl.Provider_ID
JOIN claims c ON fl.Food_ID = c.Food_ID
WHERE c.Status = 'Completed'
GROUP BY p.Provider_ID
ORDER BY completed_claims DESC;

-- 10. Percentage of claims by status
SELECT Status, COUNT(*) * 100.0 / (SELECT COUNT(*) FROM claims) AS pct
FROM claims
GROUP BY Status;

-- 11. Average quantity of food claimed per receiver
SELECT c.Receiver_ID, r.Name, AVG(fl.Quantity) AS avg_quantity
FROM claims c
JOIN food_listings fl ON c.Food_ID = fl.Food_ID
JOIN receivers r ON c.Receiver_ID = r.Receiver_ID
GROUP BY c.Receiver_ID;

-- 12. Which meal type is claimed the most?
SELECT fl.Meal_Type, COUNT(c.Claim_ID) AS claim_count
FROM food_listings fl
JOIN claims c ON fl.Food_ID = c.Food_ID
GROUP BY fl.Meal_Type
ORDER BY claim_count DESC;

-- 13. Total quantity donated by each provider
SELECT p.Provider_ID, p.Name, SUM(fl.Quantity) AS total_donated
FROM providers p
JOIN food_listings fl ON p.Provider_ID = fl.Provider_ID
GROUP BY p.Provider_ID
ORDER BY total_donated DESC;

-- 14. Food nearing expiry in next 7 days
SELECT * FROM food_listings WHERE DATE(Expiry_Date) <= DATE('now', '+7 days');

-- 15. Recent claims (last 30 days)
SELECT * FROM claims WHERE DATETIME(Timestamp) >= DATETIME('now', '-30 days');
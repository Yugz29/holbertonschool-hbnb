-- ========================
-- HBnB CRUD Test Script
-- ========================

-- Table Place
-- Add a new place
INSERT INTO Place (id, title, description, price, latitude, longitude, owner_id)
VALUES (UUID(), 'Test Apartment', 'Test apartment downtown', 50.00, 48.8566, 2.3522, '36c9050e-ddd3-4c3b-9731-9f487208bbc1');

-- Check insertion
SELECT * FROM Place;

-- Update the price
UPDATE Place SET price = 55.00 WHERE title = 'Test Apartment';

-- Check update
SELECT * FROM Place WHERE title = 'Test Apartment';

-- Table Review
-- Add a review
INSERT INTO Review (id, text, rating, user_id, place_id)
VALUES (
    UUID(),
    'Great place!',
    5,
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    (SELECT id FROM Place WHERE title = 'Test Apartment' LIMIT 1)
);

-- Check insertion
SELECT * FROM Review;

-- Update the review
UPDATE Review SET rating = 4 WHERE text = 'Great place!';

-- Delete the review
DELETE FROM Review WHERE text = 'Great place!';

-- Table Place_Amenity (Many-to-Many)
-- Link a place to an amenity
INSERT INTO Place_Amenity (place_id, amenity_id)
VALUES (
    (SELECT id FROM Place WHERE title = 'Test Apartment' LIMIT 1),
    (SELECT id FROM Amenity WHERE name = 'WiFi')
);

-- Check insertion
SELECT * FROM Place_Amenity;

-- Delete the link
DELETE FROM Place_Amenity
WHERE place_id = (SELECT id FROM Place WHERE title = 'Test Apartment' LIMIT 1)
AND amenity_id = (SELECT id FROM Amenity WHERE name = 'WiFi');

-- Cleanup: remove the test place
DELETE FROM Place WHERE title = 'Test Apartment';

-- Final verification
SELECT * FROM User;
SELECT * FROM Place;
SELECT * FROM Review;
SELECT * FROM Amenity;
SELECT * FROM Place_Amenity;
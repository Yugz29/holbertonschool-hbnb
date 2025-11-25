-- ========================
-- HBnB CRUD Test Script (Version corrigée)
-- ========================

-- Nettoyage préalable
DELETE FROM place_amenities 
WHERE place_id IN (SELECT id FROM places WHERE title = 'Test Apartment');

DELETE FROM reviews 
WHERE place_id IN (SELECT id FROM places WHERE title = 'Test Apartment');

DELETE FROM places WHERE title = 'Test Apartment';

-- ========================
-- 1. TEST: Create Place
-- ========================

-- Vérifier qu'un user existe (prendre le premier disponible)
SET @test_user_id = (SELECT id FROM users LIMIT 1);

-- Si aucun user n'existe, en créer un
INSERT INTO users (id, first_name, last_name, email, password, is_admin)
SELECT UUID(), 'Test', 'Owner', 'test_owner@hbnb.com', 'hashed_pass', 0
WHERE NOT EXISTS (SELECT 1 FROM users WHERE email = 'test_owner@hbnb.com');

-- Utiliser le user de test
SET @test_user_id = (SELECT id FROM users WHERE email = 'test_owner@hbnb.com');

-- Créer un place de test
INSERT INTO places (id, title, description, price, latitude, longitude, owner_id)
VALUES (UUID(), 'Test Apartment', 'Test apartment downtown', 50.00, 48.8566, 2.3522, @test_user_id);

-- Vérifier l'insertion
SELECT 'Created place:' AS status;
SELECT * FROM places WHERE title = 'Test Apartment';

-- ========================
-- 2. TEST: Update Place
-- ========================

-- Modifier le prix
UPDATE places SET price = 55.00 WHERE title = 'Test Apartment';

-- Vérifier la modification
SELECT 'Updated price:' AS status;
SELECT * FROM places WHERE title = 'Test Apartment';

-- ========================
-- 3. TEST: Create Review
-- ========================

-- Récupérer l'ID du place
SET @test_place_id = (SELECT id FROM places WHERE title = 'Test Apartment' LIMIT 1);

-- Créer un deuxième user pour la review (on ne peut pas reviewer son propre place)
INSERT INTO users (id, first_name, last_name, email, password, is_admin)
SELECT UUID(), 'Test', 'Reviewer', 'test_reviewer@hbnb.com', 'hashed_pass', 0
WHERE NOT EXISTS (SELECT 1 FROM users WHERE email = 'test_reviewer@hbnb.com');

SET @test_reviewer_id = (SELECT id FROM users WHERE email = 'test_reviewer@hbnb.com');

-- Créer une review
INSERT INTO reviews (id, text, rating, user_id, place_id)
VALUES (UUID(), 'Great place!', 5, @test_reviewer_id, @test_place_id);

-- Vérifier l'insertion
SELECT 'Created review:' AS status;
SELECT * FROM reviews WHERE place_id = @test_place_id;

-- ========================
-- 4. TEST: Update Review
-- ========================

-- Modifier la note
UPDATE reviews SET rating = 4 WHERE text = 'Great place!';

-- Vérifier la modification
SELECT 'Updated review:' AS status;
SELECT * FROM reviews WHERE text = 'Great place!';

-- ========================
-- 5. TEST: Many-to-Many (Place-Amenity)
-- ========================

-- Vérifier qu'une amenity WiFi existe
INSERT INTO amenities (id, name)
SELECT UUID(), 'WiFi'
WHERE NOT EXISTS (SELECT 1 FROM amenities WHERE name = 'WiFi');

-- Lier le place à l'amenity
INSERT INTO place_amenities (place_id, amenity_id)
VALUES (
    @test_place_id,
    (SELECT id FROM amenities WHERE name = 'WiFi' LIMIT 1)
);

-- Vérifier la liaison
SELECT 'Linked amenity:' AS status;
SELECT p.title, a.name 
FROM places p
JOIN place_amenities pa ON p.id = pa.place_id
JOIN amenities a ON pa.amenity_id = a.id
WHERE p.id = @test_place_id;

-- ========================
-- 6. TEST: Delete Operations
-- ========================

-- Supprimer la liaison
DELETE FROM place_amenities
WHERE place_id = @test_place_id
AND amenity_id = (SELECT id FROM amenities WHERE name = 'WiFi' LIMIT 1);

SELECT 'Deleted amenity link' AS status;

-- Supprimer la review
DELETE FROM reviews WHERE text = 'Great place!';

SELECT 'Deleted review' AS status;

-- Supprimer le place (cascade supprimera aussi les reviews restantes)
DELETE FROM places WHERE title = 'Test Apartment';

SELECT 'Deleted place' AS status;

-- ========================
-- 7. Vérification finale
-- ========================

SELECT 'Final state - Users:' AS status;
SELECT COUNT(*) AS user_count FROM users;

SELECT 'Final state - Places:' AS status;
SELECT COUNT(*) AS place_count FROM places;

SELECT 'Final state - Reviews:' AS status;
SELECT COUNT(*) AS review_count FROM reviews;

SELECT 'Final state - Amenities:' AS status;
SELECT COUNT(*) AS amenity_count FROM amenities;

SELECT 'Final state - Place-Amenities:' AS status;
SELECT COUNT(*) AS link_count FROM place_amenities;

SELECT '========================' AS status;
SELECT 'CRUD Test completed successfully!' AS status;
SELECT '========================' AS status;

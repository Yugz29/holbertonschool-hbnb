#!/usr/bin/env python3
"""
HBnB Database Population Script
================================
Creates realistic test data for the HBnB application including:
- 1 admin user
- 5 regular users
- 12 places with various amenities
- 20+ reviews
- 8 amenities

Usage:
    python scripts/populate_db.py

Requirements:
    - MySQL/MariaDB running
    - Database 'hbnb_dev' created
    - Schema already applied (hbnb_schema.sql)
"""

import sys
import os
from datetime import datetime
import uuid

# Add parent directory to path to import app modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models.user import User
from app.models.place import Place
from app.models.amenity import Amenity
from app.models.review import Review
from werkzeug.security import generate_password_hash

# =====================================
# Test Data Configuration
# =====================================

USERS_DATA = [
    {
        "email": "admin@hbnb.com",
        "password": "Admin123!",
        "first_name": "Admin",
        "last_name": "Super",
        "is_admin": True
    },
    {
        "email": "john.doe@hbnb.com",
        "password": "User123!",
        "first_name": "John",
        "last_name": "Doe",
        "is_admin": False
    },
    {
        "email": "jane.smith@hbnb.com",
        "password": "User123!",
        "first_name": "Jane",
        "last_name": "Smith",
        "is_admin": False
    },
    {
        "email": "bob.wilson@hbnb.com",
        "password": "User123!",
        "first_name": "Bob",
        "last_name": "Wilson",
        "is_admin": False
    },
    {
        "email": "alice.brown@hbnb.com",
        "password": "User123!",
        "first_name": "Alice",
        "last_name": "Brown",
        "is_admin": False
    },
    {
        "email": "charlie.davis@hbnb.com",
        "password": "User123!",
        "first_name": "Charlie",
        "last_name": "Davis",
        "is_admin": False
    }
]

AMENITIES_DATA = [
    "WiFi",
    "Kitchen",
    "Air Conditioning",
    "Heating",
    "Parking",
    "Pool",
    "Gym",
    "Pet Friendly"
]

PLACES_DATA = [
    {
        "title": "Cozy Studio in Paris",
        "description": "Perfect for solo travelers. Located in the heart of Montmartre with stunning city views.",
        "price": 75.00,
        "latitude": 48.8566,
        "longitude": 2.3522,
        "owner_email": "john.doe@hbnb.com",
        "amenities": ["WiFi", "Kitchen", "Heating"]
    },
    {
        "title": "Luxury Apartment Near Eiffel Tower",
        "description": "Spacious 3-bedroom apartment with balcony overlooking the Eiffel Tower. Perfect for families.",
        "price": 250.00,
        "latitude": 48.8584,
        "longitude": 2.2945,
        "owner_email": "john.doe@hbnb.com",
        "amenities": ["WiFi", "Kitchen", "Air Conditioning", "Heating", "Parking"]
    },
    {
        "title": "Modern Loft in Le Marais",
        "description": "Stylish loft in the trendy Marais district. Walking distance to cafes and boutiques.",
        "price": 120.00,
        "latitude": 48.8606,
        "longitude": 2.3522,
        "owner_email": "jane.smith@hbnb.com",
        "amenities": ["WiFi", "Air Conditioning", "Heating"]
    },
    {
        "title": "Charming House with Garden",
        "description": "Peaceful 2-bedroom house with private garden. Ideal for nature lovers.",
        "price": 150.00,
        "latitude": 48.8499,
        "longitude": 2.3370,
        "owner_email": "jane.smith@hbnb.com",
        "amenities": ["WiFi", "Kitchen", "Parking", "Pet Friendly"]
    },
    {
        "title": "Penthouse with Rooftop Terrace",
        "description": "Exclusive penthouse with 360° views of Paris. Private rooftop terrace with jacuzzi.",
        "price": 500.00,
        "latitude": 48.8738,
        "longitude": 2.2950,
        "owner_email": "bob.wilson@hbnb.com",
        "amenities": ["WiFi", "Kitchen", "Air Conditioning", "Heating", "Pool", "Gym"]
    },
    {
        "title": "Budget-Friendly Room in Belleville",
        "description": "Clean and comfortable room in multicultural Belleville. Great for backpackers.",
        "price": 35.00,
        "latitude": 48.8720,
        "longitude": 2.3828,
        "owner_email": "bob.wilson@hbnb.com",
        "amenities": ["WiFi", "Heating"]
    },
    {
        "title": "Family Apartment Near Louvre",
        "description": "Spacious 4-bedroom apartment. 5 minutes walk to the Louvre Museum.",
        "price": 300.00,
        "latitude": 48.8606,
        "longitude": 2.3376,
        "owner_email": "alice.brown@hbnb.com",
        "amenities": ["WiFi", "Kitchen", "Air Conditioning", "Heating", "Parking"]
    },
    {
        "title": "Artist's Studio in Montparnasse",
        "description": "Creative space with natural light. Perfect for artists and photographers.",
        "price": 90.00,
        "latitude": 48.8422,
        "longitude": 2.3219,
        "owner_email": "alice.brown@hbnb.com",
        "amenities": ["WiFi", "Heating"]
    },
    {
        "title": "Riverside Apartment with Balcony",
        "description": "Beautiful apartment along the Seine River. Enjoy breakfast on the balcony.",
        "price": 180.00,
        "latitude": 48.8534,
        "longitude": 2.3488,
        "owner_email": "charlie.davis@hbnb.com",
        "amenities": ["WiFi", "Kitchen", "Air Conditioning", "Heating"]
    },
    {
        "title": "Minimalist Suite in La Défense",
        "description": "Modern suite in business district. Perfect for professionals.",
        "price": 110.00,
        "latitude": 48.8920,
        "longitude": 2.2380,
        "owner_email": "charlie.davis@hbnb.com",
        "amenities": ["WiFi", "Air Conditioning", "Gym", "Parking"]
    },
    {
        "title": "Historic Apartment in Latin Quarter",
        "description": "Charming apartment in 18th-century building. Steps from Sorbonne University.",
        "price": 140.00,
        "latitude": 48.8510,
        "longitude": 2.3447,
        "owner_email": "john.doe@hbnb.com",
        "amenities": ["WiFi", "Kitchen", "Heating"]
    },
    {
        "title": "Pet-Friendly Cottage in Suburbs",
        "description": "Cozy cottage with fenced yard. Perfect for families with pets.",
        "price": 95.00,
        "latitude": 48.8156,
        "longitude": 2.3636,
        "owner_email": "jane.smith@hbnb.com",
        "amenities": ["WiFi", "Kitchen", "Heating", "Parking", "Pet Friendly"]
    }
]

REVIEWS_DATA = [
    {
        "place_title": "Cozy Studio in Paris",
        "reviewer_email": "jane.smith@hbnb.com",
        "rating": 5,
        "text": "Amazing location! The view of Sacré-Cœur from the window is breathtaking. Highly recommended!"
    },
    {
        "place_title": "Cozy Studio in Paris",
        "reviewer_email": "bob.wilson@hbnb.com",
        "rating": 4,
        "text": "Great place for a solo trip. A bit small but very cozy and clean."
    },
    {
        "place_title": "Luxury Apartment Near Eiffel Tower",
        "reviewer_email": "alice.brown@hbnb.com",
        "rating": 5,
        "text": "Absolutely stunning! The view of the Eiffel Tower is worth every penny. Perfect for our family vacation."
    },
    {
        "place_title": "Luxury Apartment Near Eiffel Tower",
        "reviewer_email": "charlie.davis@hbnb.com",
        "rating": 5,
        "text": "Best Airbnb experience in Paris! The host was very helpful and the apartment exceeded our expectations."
    },
    {
        "place_title": "Modern Loft in Le Marais",
        "reviewer_email": "john.doe@hbnb.com",
        "rating": 4,
        "text": "Stylish and well-located. Loved the neighborhood! Only downside: a bit noisy at night."
    },
    {
        "place_title": "Modern Loft in Le Marais",
        "reviewer_email": "bob.wilson@hbnb.com",
        "rating": 5,
        "text": "Perfect for exploring the trendy side of Paris. Walking distance to everything!"
    },
    {
        "place_title": "Charming House with Garden",
        "reviewer_email": "alice.brown@hbnb.com",
        "rating": 5,
        "text": "Peaceful oasis in the city. Our kids loved playing in the garden. Highly recommend for families!"
    },
    {
        "place_title": "Charming House with Garden",
        "reviewer_email": "charlie.davis@hbnb.com",
        "rating": 4,
        "text": "Very relaxing stay. The garden is beautiful. A bit far from the center but worth it."
    },
    {
        "place_title": "Penthouse with Rooftop Terrace",
        "reviewer_email": "jane.smith@hbnb.com",
        "rating": 5,
        "text": "Luxury at its finest! The rooftop jacuzzi under the stars was unforgettable."
    },
    {
        "place_title": "Penthouse with Rooftop Terrace",
        "reviewer_email": "john.doe@hbnb.com",
        "rating": 5,
        "text": "Worth every cent! Perfect for a romantic getaway or special celebration."
    },
    {
        "place_title": "Budget-Friendly Room in Belleville",
        "reviewer_email": "alice.brown@hbnb.com",
        "rating": 4,
        "text": "Great value for money! The neighborhood is vibrant and the host was very welcoming."
    },
    {
        "place_title": "Budget-Friendly Room in Belleville",
        "reviewer_email": "jane.smith@hbnb.com",
        "rating": 3,
        "text": "Decent for the price. Room is small but clean. Good for short stays."
    },
    {
        "place_title": "Family Apartment Near Louvre",
        "reviewer_email": "bob.wilson@hbnb.com",
        "rating": 5,
        "text": "Perfect location for sightseeing! We could walk to most attractions. Spacious and comfortable."
    },
    {
        "place_title": "Family Apartment Near Louvre",
        "reviewer_email": "charlie.davis@hbnb.com",
        "rating": 5,
        "text": "Excellent apartment for families. Well-equipped kitchen saved us money on dining out."
    },
    {
        "place_title": "Artist's Studio in Montparnasse",
        "reviewer_email": "john.doe@hbnb.com",
        "rating": 4,
        "text": "Unique and inspiring space. The natural light is amazing for photography."
    },
    {
        "place_title": "Artist's Studio in Montparnasse",
        "reviewer_email": "jane.smith@hbnb.com",
        "rating": 5,
        "text": "Loved the bohemian vibe! Perfect for creative souls. Very quiet and peaceful."
    },
    {
        "place_title": "Riverside Apartment with Balcony",
        "reviewer_email": "alice.brown@hbnb.com",
        "rating": 5,
        "text": "Waking up to the Seine River view was magical! Beautiful apartment in every way."
    },
    {
        "place_title": "Riverside Apartment with Balcony",
        "reviewer_email": "bob.wilson@hbnb.com",
        "rating": 4,
        "text": "Great location and lovely balcony. A bit pricey but worth it for the view."
    },
    {
        "place_title": "Minimalist Suite in La Défense",
        "reviewer_email": "jane.smith@hbnb.com",
        "rating": 4,
        "text": "Very modern and clean. Perfect for business trips. Easy access to metro."
    },
    {
        "place_title": "Minimalist Suite in La Défense",
        "reviewer_email": "charlie.davis@hbnb.com",
        "rating": 5,
        "text": "Exactly what I needed for my work conference. Quiet, professional, and well-equipped."
    },
    {
        "place_title": "Historic Apartment in Latin Quarter",
        "reviewer_email": "alice.brown@hbnb.com",
        "rating": 5,
        "text": "Charming apartment with so much character! Loved the historic details and location."
    },
    {
        "place_title": "Historic Apartment in Latin Quarter",
        "reviewer_email": "bob.wilson@hbnb.com",
        "rating": 4,
        "text": "Great for experiencing authentic Parisian life. The neighborhood is lively and full of history."
    },
    {
        "place_title": "Pet-Friendly Cottage in Suburbs",
        "reviewer_email": "john.doe@hbnb.com",
        "rating": 5,
        "text": "Our dog loved the fenced yard! Peaceful location and very accommodating host."
    },
    {
        "place_title": "Pet-Friendly Cottage in Suburbs",
        "reviewer_email": "charlie.davis@hbnb.com",
        "rating": 4,
        "text": "Nice quiet retreat from the city. Perfect for families with pets."
    }
]


# =====================================
# Helper Functions
# =====================================

def clear_database():
    """Clear all existing data from database"""
    print("Clearing existing data...")
    try:
        db.session.query(Review).delete()
        db.session.query(Place).delete()
        db.session.query(Amenity).delete()
        db.session.query(User).delete()
        db.session.commit()
        print("[OK] Database cleared")
    except Exception as e:
        db.session.rollback()
        print(f"[ERROR] Failed to clear database: {e}")
        sys.exit(1)


def create_users():
    """Create test users"""
    print("\nCreating users...")
    users = {}
    
    for user_data in USERS_DATA:
        try:
            user = User(
                id=str(uuid.uuid4()),
                email=user_data["email"],
                password=generate_password_hash(user_data["password"]),
                first_name=user_data["first_name"],
                last_name=user_data["last_name"],
                is_admin=user_data["is_admin"]
            )
            db.session.add(user)
            users[user_data["email"]] = user
            
            role = "Admin" if user.is_admin else "User"
            print(f"  [OK] {role}: {user.first_name} {user.last_name} ({user.email})")
        
        except Exception as e:
            print(f"  [ERROR] Failed to create user {user_data['email']}: {e}")
            db.session.rollback()
            sys.exit(1)
    
    db.session.commit()
    print(f"[OK] Created {len(users)} users")
    return users


def create_amenities():
    """Create amenities"""
    print("\nCreating amenities...")
    amenities = {}
    
    for amenity_name in AMENITIES_DATA:
        try:
            amenity = Amenity(
                id=str(uuid.uuid4()),
                name=amenity_name
            )
            db.session.add(amenity)
            amenities[amenity_name] = amenity
            print(f"  [OK] {amenity_name}")
        
        except Exception as e:
            print(f"  [ERROR] Failed to create amenity {amenity_name}: {e}")
            db.session.rollback()
            sys.exit(1)
    
    db.session.commit()
    print(f"[OK] Created {len(amenities)} amenities")
    return amenities


def create_places(users, amenities):
    """Create places with amenities"""
    print("\nCreating places...")
    places = {}
    
    for place_data in PLACES_DATA:
        try:
            owner = users.get(place_data["owner_email"])
            if not owner:
                print(f"  [WARNING] Owner not found: {place_data['owner_email']}")
                continue
            
            place = Place(
                id=str(uuid.uuid4()),
                title=place_data["title"],
                description=place_data["description"],
                price=place_data["price"],
                latitude=place_data["latitude"],
                longitude=place_data["longitude"],
                owner_id=owner.id
            )
            
            # Add amenities
            for amenity_name in place_data.get("amenities", []):
                amenity = amenities.get(amenity_name)
                if amenity:
                    place.amenities.append(amenity)
            
            db.session.add(place)
            places[place_data["title"]] = place
            
            amenities_count = len(place_data.get("amenities", []))
            print(f"  [OK] {place.title} (${place.price}/night) - {amenities_count} amenities")
        
        except Exception as e:
            print(f"  [ERROR] Failed to create place {place_data['title']}: {e}")
            db.session.rollback()
            sys.exit(1)
    
    db.session.commit()
    print(f"[OK] Created {len(places)} places")
    return places


def create_reviews(users, places):
    """Create reviews"""
    print("\nCreating reviews...")
    review_count = 0
    
    for review_data in REVIEWS_DATA:
        try:
            reviewer = users.get(review_data["reviewer_email"])
            place = places.get(review_data["place_title"])
            
            if not reviewer:
                print(f"  [WARNING] Reviewer not found: {review_data['reviewer_email']}")
                continue
            
            if not place:
                print(f"  [WARNING] Place not found: {review_data['place_title']}")
                continue
            
            # Check if user owns the place
            if place.owner_id == reviewer.id:
                print(f"  [SKIP] {reviewer.first_name} cannot review their own place")
                continue
            
            review = Review(
                id=str(uuid.uuid4()),
                text=review_data["text"],
                rating=review_data["rating"],
                user_id=reviewer.id,
                place_id=place.id
            )
            
            db.session.add(review)
            review_count += 1
            
            print(f"  [OK] {reviewer.first_name} -> {place.title} ({review_data['rating']}/5)")
        
        except Exception as e:
            print(f"  [WARNING] Failed to create review: {e}")
            db.session.rollback()
            continue
    
    db.session.commit()
    print(f"[OK] Created {review_count} reviews")


# =====================================
# Main Population Function
# =====================================

def populate_database():
    """Main function to populate database"""
    print("=" * 60)
    print("HBnB Database Population Script")
    print("=" * 60)
    
    clear_database()
    users = create_users()
    amenities = create_amenities()
    places = create_places(users, amenities)
    create_reviews(users, places)
    
    print("\n" + "=" * 60)
    print("Database population completed successfully!")
    print("=" * 60)
    print("\nSummary:")
    print(f"  - Users: {len(users)}")
    print(f"  - Places: {len(places)}")
    print(f"  - Amenities: {len(amenities)}")
    print(f"  - Reviews: {db.session.query(Review).count()}")
    print("\nTest Credentials:")
    print("  Admin:")
    print("    Email: admin@hbnb.com")
    print("    Password: Admin123!")
    print("  Regular User:")
    print("    Email: john.doe@hbnb.com")
    print("    Password: User123!")
    print("\nStart the application with: python run.py")
    print("=" * 60)


# =====================================
# Script Entry Point
# =====================================

if __name__ == "__main__":
    app = create_app()
    
    with app.app_context():
        try:
            populate_database()
        except KeyboardInterrupt:
            print("\n\nPopulation interrupted by user")
            sys.exit(0)
        except Exception as e:
            print(f"\nFatal error: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)

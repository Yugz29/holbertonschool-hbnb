#!/usr/bin/env python3
"""HBnB Database Population Script"""

import sys
import os
from datetime import datetime
import uuid
import random

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
from werkzeug.security import generate_password_hash

# Password hash method
HASH_METHOD = "pbkdf2:sha256"


def clear_database():
    """Clear all existing data"""
    print("Clearing existing data...")
    try:
        try:
            db.session.execute(db.text('DELETE FROM place_amenity'))
        except:
            pass
        
        try:
            Review.query.delete()
        except:
            pass
        
        try:
            Place.query.delete()
        except:
            pass
        
        try:
            Amenity.query.delete()
        except:
            pass
        
        try:
            User.query.delete()
        except:
            pass
        
        db.session.commit()
        print("  [OK] Database cleared\n")
    except Exception as e:
        db.session.rollback()
        print(f"  [WARNING] {e}\n")


def create_users():
    """Create sample users"""
    print("Creating users...")
    
    users_data = [
        {
            'email': 'admin@hbnb.com',
            'password': 'admin123',
            'first_name': 'Admin',
            'last_name': 'HBnB',
            'is_admin': True
        },
        {
            'email': 'john.doe@example.com',
            'password': 'password123',
            'first_name': 'John',
            'last_name': 'Doe',
            'is_admin': False
        },
        {
            'email': 'jane.smith@example.com',
            'password': 'password123',
            'first_name': 'Jane',
            'last_name': 'Smith',
            'is_admin': False
        },
        {
            'email': 'bob.wilson@example.com',
            'password': 'password123',
            'first_name': 'Bob',
            'last_name': 'Wilson',
            'is_admin': False
        },
        {
            'email': 'alice.brown@example.com',
            'password': 'password123',
            'first_name': 'Alice',
            'last_name': 'Brown',
            'is_admin': False
        },
        {
            'email': 'charlie.davis@example.com',
            'password': 'password123',
            'first_name': 'Charlie',
            'last_name': 'Davis',
            'is_admin': False
        }
    ]
    
    created_users = []
    for user_data in users_data:
        try:
            user = User(
                id=str(uuid.uuid4()),
                email=user_data['email'],
                password=generate_password_hash(user_data['password'], method=HASH_METHOD),
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                is_admin=user_data['is_admin']
            )
            db.session.add(user)
            db.session.commit()
            created_users.append(user)
            print(f"  [OK] Created user: {user.email}")
        except Exception as e:
            db.session.rollback()
            print(f"  [ERROR] Failed to create user {user_data['email']}: {e}")
    
    print(f"\n✅ Created {len(created_users)} users\n")
    return created_users


def create_amenities():
    """Create sample amenities"""
    print("Creating amenities...")
    
    amenities_list = [
        'WiFi', 'Air Conditioning', 'Heating', 'Kitchen',
        'Washing Machine', 'Dryer', 'TV', 'Pool', 'Gym',
        'Parking', 'Elevator', 'Balcony', 'Garden',
        'Fireplace', 'Hot Tub'
    ]
    
    created_amenities = []
    for name in amenities_list:
        try:
            amenity = Amenity(
                id=str(uuid.uuid4()),
                name=name
            )
            db.session.add(amenity)
            db.session.commit()
            created_amenities.append(amenity)
            print(f"  [OK] Created amenity: {name}")
        except Exception as e:
            db.session.rollback()
            print(f"  [ERROR] Failed to create amenity {name}: {e}")
    
    print(f"\n✅ Created {len(created_amenities)} amenities\n")
    return created_amenities


def create_places(users, amenities):
    """Create sample places"""
    print("Creating places...")
    
    if not users:
        print("  [ERROR] No users available to create places\n")
        return []
    
    places_data = [
        {
            'title': 'Cozy Studio in Paris',
            'description': 'A comfortable studio apartment in the heart of Paris',
            'price': 75.0,
            'latitude': 48.8566,
            'longitude': 2.3522
        },
        {
            'title': 'Modern Apartment Downtown',
            'description': 'Stylish 2-bedroom apartment with city views',
            'price': 120.0,
            'latitude': 48.8584,
            'longitude': 2.2945
        },
        {
            'title': 'Beach House Paradise',
            'description': 'Beautiful beach house with ocean views',
            'price': 200.0,
            'latitude': 43.2965,
            'longitude': 5.3698
        },
        {
            'title': 'Mountain Cabin Retreat',
            'description': 'Peaceful cabin in the mountains',
            'price': 90.0,
            'latitude': 45.1885,
            'longitude': 5.7245
        },
        {
            'title': 'Luxury Penthouse',
            'description': 'High-end penthouse with panoramic views',
            'price': 350.0,
            'latitude': 48.8606,
            'longitude': 2.3376
        },
        {
            'title': 'Charming Cottage',
            'description': 'Rustic cottage in countryside',
            'price': 65.0,
            'latitude': 48.8738,
            'longitude': 2.2950
        },
        {
            'title': 'Urban Loft',
            'description': 'Industrial-style loft in trendy neighborhood',
            'price': 110.0,
            'latitude': 48.8566,
            'longitude': 2.3522
        },
        {
            'title': 'Family Villa',
            'description': 'Spacious villa perfect for families',
            'price': 180.0,
            'latitude': 43.6047,
            'longitude': 1.4442
        }
    ]
    
    created_places = []
    for i, place_data in enumerate(places_data):
        try:
            owner = users[i % len(users)]
            
            place = Place(
                id=str(uuid.uuid4()),
                title=place_data['title'],
                description=place_data['description'],
                price=place_data['price'],
                latitude=place_data['latitude'],
                longitude=place_data['longitude'],
                owner_id=owner.id
            )
            
            # Add random amenities (3-5 per place)
            if amenities:
                num_amenities = random.randint(3, min(5, len(amenities)))
                selected_amenities = random.sample(amenities, num_amenities)
                place.amenities.extend(selected_amenities)
            
            db.session.add(place)
            db.session.commit()
            created_places.append(place)
            print(f"  [OK] Created place: {place.title} (Owner: {owner.email})")
        except Exception as e:
            db.session.rollback()
            print(f"  [ERROR] Failed to create place: {e}")
    
    print(f"\n✅ Created {len(created_places)} places\n")
    return created_places


def create_reviews(users, places):
    """Create sample reviews"""
    print("Creating reviews...")
    
    if not users or not places:
        print("  [ERROR] No users or places available to create reviews\n")
        return []
    
    reviews_data = [
        {'comment': 'Great place, very comfortable!', 'rating': 5},
        {'comment': 'Nice location but a bit noisy', 'rating': 3},
        {'comment': 'Perfect for a weekend getaway', 'rating': 4},
        {'comment': 'Excellent host, highly recommended', 'rating': 5},
        {'comment': 'Good value for money', 'rating': 4},
        {'comment': 'Could be cleaner', 'rating': 2},
        {'comment': 'Amazing views and very spacious', 'rating': 5},
        {'comment': 'Decent place, nothing special', 'rating': 3},
        {'comment': 'Loved every minute of our stay', 'rating': 5},
        {'comment': 'Not as described, disappointed', 'rating': 2},
        {'comment': 'Perfect location and amenities', 'rating': 5}
    ]
    
    created_reviews = []
    for i, review_data in enumerate(reviews_data):
        try:
            place = places[i % len(places)]
            user_index = (i + 1) % len(users)
            reviewer = users[user_index]
            
            # Skip if user is reviewing their own place
            if place.owner_id == reviewer.id:
                print(f"  [SKIP] User cannot review their own place")
                continue
            
            review = Review(
                id=str(uuid.uuid4()),
                text=review_data['comment'],
                rating=review_data['rating'],
                user_id=reviewer.id,
                place_id=place.id
            )
            db.session.add(review)
            db.session.commit()
            created_reviews.append(review)
            print(f"  [OK] Created review for '{place.title}' by {reviewer.email}")
        except Exception as e:
            db.session.rollback()
            print(f"  [ERROR] Failed to create review: {e}")
    
    print(f"\n✅ Created {len(created_reviews)} reviews\n")
    return created_reviews


def main():
    """Main population function"""
    print("\n" + "="*60)
    print("HBnB Database Population Script")
    print("="*60 + "\n")
    
    app = create_app()
    with app.app_context():
        try:
            clear_database()
            users = create_users()
            amenities = create_amenities()
            places = create_places(users, amenities)
            reviews = create_reviews(users, places)
            
            print("\n" + "="*60)
            print("✅ Database population completed successfully!")
            print("="*60)
            print(f"\nSummary:")
            print(f"  - Users: {len(users)}")
            print(f"  - Amenities: {len(amenities)}")
            print(f"  - Places: {len(places)}")
            print(f"  - Reviews: {len(reviews)}")
            print(f"\n💡 Admin login: admin@hbnb.com / admin123")
            print(f"💡 Test user: john.doe@example.com / password123\n")
            
        except Exception as e:
            print(f"\n❌ Population failed: {e}\n")
            import traceback
            traceback.print_exc()
            sys.exit(1)


if __name__ == '__main__':
    main()

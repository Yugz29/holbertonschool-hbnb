import uuid

# Password hash method constant
HASH_METHOD = "pbkdf2:sha256"
from app import create_app, db
from app.models.user import User
from app.models.place import Place
from app.models.amenity import Amenity
from app.models.associations import place_amenity as PlaceAmenity
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    # -----------------------------
    # Users
    # -----------------------------
    admin = User(
        id=str(uuid.uuid4()),
        first_name="Admin",
        last_name="HBnB",
        email="admin@hbnb.io",
        password=generate_password_hash("adminpassword", method=HASH_METHOD),
        is_admin=True
    )

    users = [
        User(id=str(uuid.uuid4()), first_name="Alice", last_name="Dupont", email="user1@example.com", password=generate_password_hash("user1password", method=HASH_METHOD)),
        User(id=str(uuid.uuid4()), first_name="Bob", last_name="Martin", email="user2@example.com", password=generate_password_hash("user2password", method=HASH_METHOD)),
        User(id=str(uuid.uuid4()), first_name="Charlie", last_name="Durand", email="user3@example.com", password=generate_password_hash("user3password", method=HASH_METHOD)),
    ]

    db.session.add(admin)
    db.session.add_all(users)
    db.session.commit()

    # -----------------------------
    # Amenities
    # -----------------------------
    amenities = [
        Amenity(id=str(uuid.uuid4()), name="WiFi"),
        Amenity(id=str(uuid.uuid4()), name="Swimming Pool"),
        Amenity(id=str(uuid.uuid4()), name="Air Conditioning"),
        Amenity(id=str(uuid.uuid4()), name="Parking"),
        Amenity(id=str(uuid.uuid4()), name="TV"),
        Amenity(id=str(uuid.uuid4()), name="Kitchen"),
    ]

    db.session.add_all(amenities)
    db.session.commit()

    # -----------------------------
    # Places
    # -----------------------------
    all_users = [admin] + users
    places = [
        Place(id=str(uuid.uuid4()), title="Studio centre-ville", description="Studio lumineux", price=45, latitude=48.8566, longitude=2.3522, owner_id=users[0].id),
        Place(id=str(uuid.uuid4()), title="Appartement cosy", description="Petit appartement en centre-ville", price=70, latitude=48.8566, longitude=2.3522, owner_id=users[1].id),
        Place(id=str(uuid.uuid4()), title="Villa Bord de Mer", description="Villa spacieuse avec piscine", price=150, latitude=43.2965, longitude=5.3698, owner_id=users[0].id),
        Place(id=str(uuid.uuid4()), title="Chambre simple", description="Chambre confortable", price=30, latitude=48.8566, longitude=2.3522, owner_id=users[2].id),
        Place(id=str(uuid.uuid4()), title="Loft industriel", description="Loft moderne en ville", price=90, latitude=48.8566, longitude=2.3522, owner_id=users[1].id),
        Place(id=str(uuid.uuid4()), title="Maison de campagne", description="Maison tranquille à la campagne", price=110, latitude=46.2276, longitude=2.2137, owner_id=users[2].id),
    ]

    db.session.add_all(places)
    db.session.commit()

    # -----------------------------
    # Place_Amenities associations
    # -----------------------------
    # Example: assign random amenities to each place
    import random

    for place in places:
        selected_amenities = random.sample(amenities, 3)  # assign 3 random amenities
        for amenity in selected_amenities:
            place.amenities.append(amenity)

    db.session.commit()

    print("Database seeded successfully!")
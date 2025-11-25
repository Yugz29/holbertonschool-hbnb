# Database Population Script Documentation

## Overview

This directory contains the database initialization and population script for the HBnB Evolution application. The script creates sample data for testing and development purposes.

## Files

```
scripts/
└── populate_db.py          # Database population script
```

---

## 📄 populate_db.py

### Purpose

This script populates the database with realistic sample data including:
- **Users** (regular users and admins)
- **Places** (various properties with different characteristics)
- **Amenities** (common property features)
- **Reviews** (user feedback on places)
- **Relationships** (place-amenity associations)

### Features

- ✅ Creates initial admin user
- ✅ Generates sample users with hashed passwords
- ✅ Creates diverse place listings
- ✅ Populates common amenities
- ✅ Links amenities to places
- ✅ Generates realistic reviews
- ✅ Proper error handling
- ✅ Transaction management

---

## 🚀 Usage

### Prerequisites

1. Database must be initialized (tables created)
2. Virtual environment activated
3. All dependencies installed

```bash
# Ensure you're in the project root directory
cd /path/to/hbnb

# Activate virtual environment
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate     # Windows

# Verify dependencies
pip install -r requirements.txt
```

### Running the Script

```bash
# From project root
python scripts/populate_db.py
```

### Expected Output

```
Starting database population...
Creating admin user...
Admin created: admin@hbnb.com (ID: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx)
Creating sample users...
Created user: john.doe@example.com
Created user: jane.smith@example.com
Created user: bob.wilson@example.com
...
Creating sample places...
Created place: Cozy Studio in Paris
Created place: Beach House in Miami
...
Creating amenities...
Created amenity: WiFi
Created amenity: Air Conditioning
...
Linking amenities to places...
Linked 3 amenities to Cozy Studio in Paris
...
Creating sample reviews...
Created review for Cozy Studio in Paris
...
Database populated successfully!
```

---

## 📊 Generated Data

### Users

The script creates **10 sample users** plus **1 admin**:

| Email | Password | Role | Admin |
|-------|----------|------|-------|
| admin@hbnb.com | admin123 | Administrator | ✅ Yes |
| john.doe@example.com | password123 | User | ❌ No |
| jane.smith@example.com | password123 | User | ❌ No |
| bob.wilson@example.com | password123 | User | ❌ No |
| alice.brown@example.com | password123 | User | ❌ No |
| charlie.davis@example.com | password123 | User | ❌ No |
| diana.moore@example.com | password123 | User | ❌ No |
| eve.taylor@example.com | password123 | User | ❌ No |
| frank.anderson@example.com | password123 | User | ❌ No |
| grace.thomas@example.com | password123 | User | ❌ No |
| henry.jackson@example.com | password123 | User | ❌ No |

**Note:** All passwords are hashed using bcrypt before storage.

---

### Places

The script creates **8 diverse places**:

#### 1. Cozy Studio in Paris
- **Price:** $120/night
- **Description:** Charming studio in the heart of Paris
- **Latitude:** 48.8566
- **Longitude:** 2.3522
- **Owner:** john.doe@example.com

#### 2. Beach House in Miami
- **Price:** $250/night
- **Description:** Beautiful beach house with ocean view
- **Latitude:** 25.7617
- **Longitude:** -80.1918
- **Owner:** jane.smith@example.com

#### 3. Mountain Cabin in Colorado
- **Price:** $180/night
- **Description:** Rustic cabin in the Rocky Mountains
- **Latitude:** 39.5501
- **Longitude:** -105.7821
- **Owner:** bob.wilson@example.com

#### 4. City Loft in New York
- **Price:** $300/night
- **Description:** Modern loft in downtown Manhattan
- **Latitude:** 40.7128
- **Longitude:** -74.0060
- **Owner:** alice.brown@example.com

#### 5. Country House in Tuscany
- **Price:** $200/night
- **Description:** Traditional Italian villa with vineyard
- **Latitude:** 43.7711
- **Longitude:** 11.2486
- **Owner:** charlie.davis@example.com

#### 6. Urban Apartment in Tokyo
- **Price:** $150/night
- **Description:** Compact apartment in Shibuya
- **Latitude:** 35.6762
- **Longitude:** 139.6503
- **Owner:** diana.moore@example.com

#### 7. Desert Retreat in Arizona
- **Price:** $220/night
- **Description:** Secluded retreat with stunning desert views
- **Latitude:** 33.4484
- **Longitude:** -112.0740
- **Owner:** eve.taylor@example.com

#### 8. Lakeside Cottage in Canada
- **Price:** $190/night
- **Description:** Peaceful cottage by the lake
- **Latitude:** 45.4215
- **Longitude:** -75.6972
- **Owner:** frank.anderson@example.com

---

### Amenities

The script creates **10 common amenities**:

| Amenity | Description |
|---------|-------------|
| WiFi | High-speed wireless internet |
| Air Conditioning | Climate control system |
| Heating | Central heating system |
| Kitchen | Full kitchen with appliances |
| Washer | Washing machine |
| Dryer | Clothes dryer |
| TV | Television with cable/streaming |
| Parking | Free parking on premises |
| Pool | Swimming pool access |
| Gym | Fitness center access |

---

## 🔐 Security Considerations

### Password Hashing

All user passwords are automatically hashed using bcrypt through the User model:

```python
# In app/models/user.py
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()

class User(BaseModel):
    def __init__(self, email, password, first_name, last_name, is_admin=False):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
        # ... other attributes
```

**Important:** Never store plain-text passwords in production!

---

### Admin Account

The default admin account should be changed immediately after initial setup:

```bash
# Default credentials (CHANGE THESE!)
Email: admin@hbnb.com
Password: admin123
```

**Recommended Actions:**
1. Login as admin
2. Change password via `/api/v1/users/{id}` endpoint
3. Consider changing email as well
4. Delete or disable this account if not needed

---

## 🧪 Testing the Population

### Verify Data Creation

```bash
# Check if data was created
sqlite3 instance/development.db

# Count users
SELECT COUNT(*) FROM users;
# Expected: 11 (10 users + 1 admin)

# Count places
SELECT COUNT(*) FROM places;
# Expected: 8

# Count amenities
SELECT COUNT(*) FROM amenities;
# Expected: 10

# Count reviews
SELECT COUNT(*) FROM reviews;
# Expected: 15-20

# Check place-amenity links
SELECT COUNT(*) FROM place_amenity;
# Expected: 24-40 (3-5 per place × 8 places)
```

---

## ⚠️ Troubleshooting

### Error: "Table doesn't exist"

**Solution:** Ensure database tables are created first.

```bash
python
>>> from app import create_app, db
>>> app = create_app()
>>> with app.app_context():
>>>     db.create_all()
```

---

### Error: "Integrity constraint failed"

**Cause:** Attempting to create duplicate users or violating foreign key constraints.

**Solution:** Clear existing data before re-running the script.

---

### Error: "No module named 'app'"

**Cause:** Script run from wrong directory.

**Solution:** Always run from project root:
```bash
cd /path/to/hbnb
python scripts/populate_db.py
```

---

### Error: "Password hashing failed"

**Cause:** bcrypt not installed or configured properly.

**Solution:**
```bash
pip install flask-bcrypt
```
---

## 📚 Related Documentation

- [Main README](../README.md) - Project overview
- [API Documentation](../API.md) - API endpoints
- [Frontend Documentation](../app/static/README.md) - Frontend code
- [Database Schema](../sql/README.md) - Database structure

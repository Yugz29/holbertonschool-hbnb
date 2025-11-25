# SQL Scripts for HBnB Evolution Project

This directory contains SQL scripts for database schema management and testing CRUD operations for the HBnB Evolution application.

---

## 📁 Files

### `hbnb_schema.sql`
Database schema definition with all tables, relationships, and constraints required for the application.

**Tables created:**
- `users` - User accounts and authentication
- `places` - Property listings
- `amenities` - Property features/amenities
- `reviews` - User reviews for places
- `place_amenity` - Many-to-many relationship between places and amenities

**Features:**
- ✅ UUID primary keys
- ✅ Foreign key constraints with CASCADE
- ✅ Timestamp tracking (created_at, updated_at)
- ✅ Proper indexing for performance
- ✅ Data validation constraints

---

### `hbnb_crud_test.sql`
Comprehensive test script for validating CRUD operations across all tables.

**Test coverage:**
- ✅ INSERT operations (Create)
- ✅ SELECT queries (Read)
- ✅ UPDATE statements (Update)
- ✅ DELETE operations (Delete)
- ✅ Relationship integrity
- ✅ Constraint validation

---

## 🚀 Usage

### Prerequisites

- MySQL 5.7+ or MariaDB 10.3+
- Database user with appropriate privileges
- Database created (default: `hbnb_dev`)

---

### Initial Setup

#### 1. Create the database (if not exists)

```bash
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS hbnb_dev;"
mysql -u root -p -e "CREATE USER IF NOT EXISTS 'hbnb_dev'@'localhost' IDENTIFIED BY 'hbnb_dev_pwd';"
mysql -u root -p -e "GRANT ALL PRIVILEGES ON hbnb_dev.* TO 'hbnb_dev'@'localhost';"
mysql -u root -p -e "FLUSH PRIVILEGES;"
```

#### 2. Initialize the schema

```bash
# Using root user
mysql -u root -p hbnb_dev < sql/hbnb_schema.sql

# Or using dedicated user
mysql -u hbnb_dev -p hbnb_dev < sql/hbnb_schema.sql
```

**Expected output:**
```
Database schema created successfully!
All tables, indexes, and constraints are in place.
```

---

### Testing CRUD Operations

Run the test script to verify database functionality:

```bash
mysql -u root -p hbnb_dev < sql/hbnb_crud_test.sql
```

**With verbose output:**
```bash
mysql -u root -p hbnb_dev -vvv < sql/hbnb_crud_test.sql
```

**Expected results:**
- All INSERT operations succeed
- SELECT queries return correct data
- UPDATE operations modify records properly
- DELETE operations remove data and cascade correctly
- Constraints are enforced
- No errors or warnings

---

## 🔧 Common Operations

### View all tables

```bash
mysql -u hbnb_dev -p hbnb_dev -e "SHOW TABLES;"
```

### Check table structure

```bash
mysql -u hbnb_dev -p hbnb_dev -e "DESCRIBE users;"
mysql -u hbnb_dev -p hbnb_dev -e "DESCRIBE places;"
```

### Export database

```bash
mysqldump -u hbnb_dev -p hbnb_dev > backup_$(date +%Y%m%d).sql
```

### Drop and recreate schema

```bash
# Drop all tables
mysql -u hbnb_dev -p hbnb_dev -e "DROP DATABASE hbnb_dev;"
mysql -u hbnb_dev -p -e "CREATE DATABASE hbnb_dev;"

# Recreate schema
mysql -u hbnb_dev -p hbnb_dev < sql/hbnb_schema.sql
```

---

## 📊 Database Schema Overview

### Entity Relationship

```
┌─────────┐         ┌─────────┐         ┌───────────┐
│  users  │────────>│ places  │<────────│  reviews  │
└─────────┘ 1    N  └─────────┘  N   1  └───────────┘
                         │ N
                         │
                         │ N
                    ┌────────────────┐
                    │ place_amenity  │
                    │  (join table)  │
                    └────────────────┘
                         │ N
                         │
                         │ 1
                    ┌───────────┐
                    │ amenities │
                    └───────────┘
```

### Key Relationships

- **User → Places**: One user can own many places (1:N)
- **User → Reviews**: One user can write many reviews (1:N)
- **Place → Reviews**: One place can have many reviews (1:N)
- **Place ↔ Amenities**: Many-to-many through `place_amenity` table

---

## ⚠️ Important Notes

### Foreign Key Constraints

All foreign keys use `ON DELETE CASCADE`:
- Deleting a user removes all their places and reviews
- Deleting a place removes all its reviews and amenity links
- This ensures referential integrity

### UUID Usage

All primary keys use UUID (CHAR(36)):
- Universally unique identifiers
- No sequential ID guessing
- Better for distributed systems

### Timestamps

All tables include:
- `created_at`: Automatically set on INSERT
- `updated_at`: Automatically updated on UPDATE (via trigger)

---

## 🐛 Troubleshooting

### Error: "Access denied for user"

```bash
# Grant privileges again
mysql -u root -p -e "GRANT ALL PRIVILEGES ON hbnb_dev.* TO 'hbnb_dev'@'localhost';"
mysql -u root -p -e "FLUSH PRIVILEGES;"
```

### Error: "Table already exists"

```bash
# Drop and recreate
mysql -u hbnb_dev -p hbnb_dev -e "DROP DATABASE hbnb_dev; CREATE DATABASE hbnb_dev;"
mysql -u hbnb_dev -p hbnb_dev < sql/hbnb_schema.sql
```

### Error: "Unknown database"

```bash
# Create database first
mysql -u root -p -e "CREATE DATABASE hbnb_dev;"
```

### CRUD test fails

1. Ensure schema is properly initialized
2. Check for existing test data conflicts
3. Verify foreign key constraints are enabled:
   ```bash
   mysql -u hbnb_dev -p hbnb_dev -e "SHOW VARIABLES LIKE 'foreign_key_checks';"
   ```

---

## 📚 Related Documentation

- [Main README](../README.md) - Project overview
- [Database Population Script](../scripts/README.md) - Sample data generation
- [API Documentation](../API.md) - API endpoints using these tables


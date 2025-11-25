# 🏠 HBnB Evolution - Part 4: Simple Web Client

## Overview

**Part 4** completes the HBnB Evolution platform by building an interactive **front-end web client** using **HTML5**, **CSS3**, and **JavaScript ES6**. This client interfaces seamlessly with the RESTful API developed in **Parts 1-3**, providing users with an intuitive way to browse places, view details, and submit reviews.

The front-end implements:
- JWT-based authentication with secure cookie management
- Dynamic content rendering via Fetch API
- Client-side filtering for places
- Protected routes with automatic redirection
- Responsive design following modern web standards

---

## 📂 Project Structure

```
part4/
├── app/
│   ├── init.py                    # Flask app factory
│   ├── api/
│   │   ├── init.py
│   │   └── v1/
│   │       ├── init.py            # Blueprint registration
│   │       ├── amenities.py           # Amenities endpoints
│   │       ├── auth.py                # Authentication endpoints
│   │       ├── places.py              # Places endpoints
│   │       ├── reviews.py             # Reviews endpoints
│   │       └── users.py               # Users endpoints
│   ├── models/
│   │   ├── init.py
│   │   ├── amenity.py                 # Amenity entity
│   │   ├── base.py                    # Base entity class
│   │   ├── place.py                   # Place entity
│   │   ├── place_amenity.py           # Many-to-many relationship
│   │   ├── review.py                  # Review entity
│   │   └── user.py                    # User entity
│   ├── services/
│   │   ├── init.py
│   │   └── facade.py                  # Business logic layer
│   ├── persistence/
│   │   ├── init.py
│   │   └── repository.py              # Database operations
│   ├── static/
│   │   ├── styles.css                 # Global styles
│   │   ├── scripts.js                 # Utility functions
│   │   ├── index.js                   # Home page logic
│   │   ├── place.js                   # Place details logic
│   │   ├── login.js                   # Login page logic
│   │   ├── add-review.js              # Add review logic
│   │   └── README.md                  # Frontend documentation
│   └── templates/
│       ├── index.html                 # Home page
│       ├── place.html                 # Place details page
│       ├── login.html                 # Login/Register page
│       ├── add-review.html            # Add review page
│       └── README.md                  # Templates documentation
├── scripts/
│   ├── populate_db.py                 # Database seeding script
│   └── README.md                      # Scripts documentation
├── sql/
│   ├── schema.sql                     # Database schema
│   ├── data.sql                       # Sample data
│   └── README.md                      # SQL documentation
├── tests/
│   ├── init.py
│   ├── conftest.py                    # Pytest configuration
│   ├── test_amenities.py              # Amenities API tests
│   ├── test_auth.py                   # Authentication tests
│   ├── test_places.py                 # Places API tests
│   ├── test_reviews.py                # Reviews API tests
│   ├── test_users.py                  # Users API tests
│   └── README.md                      # Testing documentation
├── config.py                          # Application configuration
├── run.py                             # Application entry point
├── requirements.txt                   # Python dependencies
└── README.md                          # This file
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip
- SQLite3

### Installation

```bash
# Clone the repository
git clone https://github.com/Yugz29/holbertonschool-hbnb.git
cd holbertonschool-hbnb/part4

# Install dependencies
pip install -r requirements.txt

# Initialize database
sqlite3 instance/hbnb.db < sql/hbnb_schema.sql

# Populate with sample data
python3 scripts/populate_db.py

# Run the application
python3 run.py
```

### 🌐 Access the Application

Open your browser and navigate to: http://127.0.0.1:5000/index

---

## 👥 Test Accounts

### Admin User
```
Email: admin@hbnb.io
Password: admin1234
```

### Regular Users
```
Email: john.doe@example.com
Password: password123

Email: jane.smith@example.com
Password: password123
```

---

## Application Pages

| Page | Route | Description | Authentication |
|------|-------|-------------|----------------|
| Home | /index | Browse all places with country filter | Optional |
| Login | /login | User authentication | Public |
| Place Details | /place?id={id} | View place information and reviews | Optional |
| Add Review | /add_review?place_id={id} | Submit a review for a place | Required |

For detailed page documentation, see app/templates/README.md

---

## Front-End Features

### Technologies Used
- HTML5: Semantic markup and structure
- CSS3: Modern styling with Flexbox
- JavaScript ES6: Async/await, Fetch API, Cookie management

### Key Functionalities
- Dynamic content loading without page refresh
- JWT authentication with automatic token refresh
- Client-side filtering by country
- Protected routes with redirection
- Responsive design for mobile and desktop

For detailed front-end documentation, see app/static/README.md

---

## Configuration

### Environment Variables

The application uses config.py for configuration:

```python
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///instance/hbnb.db'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
```

### CORS Configuration

CORS is configured in app/__init__.py to allow requests from the front-end:

```python
CORS(app, resources={
    r"/api/*": {
        "origins": ["*"],
        "supports_credentials": True
    }
})
```

---

## 📚 Additional Documentation

- Front-End Documentation (app/static/README.md) - CSS/JS structure and functions
- Templates Documentation (app/templates/README.md) - HTML pages details
- SQL Documentation (sql/README.md) - Database schema and CRUD operations
- Scripts Documentation (scripts/README.md) - Database population utilities
- Tests Documentation (tests/README.md) - API testing guide

---

## 🧠 Learning Objectives

- Build interactive web pages with HTML5, CSS3, and JavaScript ES6
- Implement client-server communication using Fetch API
- Handle JWT authentication in a web client
- Create responsive designs following modern standards
- Manage client-side routing and protected pages
- Configure CORS for cross-origin requests

---

## License

This project is part of the Holberton School curriculum.  
All rights reserved © 2024 Holberton School.


# 🏠 HBnB part3

## Overview

The **HBnB API** is a modular Flask-based web application designed to manage core components of the HBnB platform — such as **users**, **places**, **reviews**, and **amenities**.  
This project implements a **database-backed repository** using **SQLAlchemy** for persistence, integrates **JWT authentication** for secure access, and enforces **role-based access control (RBAC)** to manage user permissions.

The architecture follows a **three-layer design**:  
- **Presentation Layer (API)** — Handles HTTP requests and responses, including authentication and authorization.  
- **Business Logic Layer (Services)** — Manages core application logic via the **Facade pattern**, coordinating between API and persistence layers.  
- **Persistence Layer (Repository)** — Uses SQLAlchemy ORM to persist and retrieve data from a relational database.

This design ensures scalability, security, maintainability, and clear separation of concerns.

---

## 📁 Project Structure

```
part3/
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── users.py
│   │   │   ├── places.py
│   │   │   ├── reviews.py
│   │   │   ├── amenities.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── place.py
│   │   ├── review.py
│   │   ├── amenity.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── facade.py
│   ├── persistence/
│       ├── __init__.py
│       ├── repository.py
├── tests/
│   ├── README.md
│   ├── test_users.py
│   ├── test_places.py
│   ├── test_reviews.py
│   ├── test_amenities.py
├── sql/
│   ├── README.md
│   ├── hbnb_crud_test.sql
│   ├── hbnb_schema.sql
├── run.py
├── config.py
├── requirements.txt
├── README.md
```

---

## 🧩 Layers Description

### **1. Presentation Layer (API)**
Located under `app/api/v1/`, this layer exposes RESTful endpoints secured with **JWT authentication**.  
It enforces **role-based access control (RBAC)** to restrict actions based on user roles (e.g., admin, user).  
Endpoints handle input validation, authentication, authorization, and response formatting.

### **2. Business Logic Layer (Services)**
Implemented in `app/services/facade.py`, the **Facade pattern** centralizes business logic operations, ensuring consistent handling of data and rules.  
It acts as an intermediary between API routes and the persistence layer, managing transactions and complex workflows.

### **3. Persistence Layer (Repository)**
Located in `app/persistence/repository.py`, this layer uses **SQLAlchemy ORM** to interact with a relational database for durable data storage.  
It provides CRUD operations for all domain models and abstracts database details from higher layers.

---

## ⚙️ Installation and Setup

### **1. Clone the Repository**

```bash
git clone https://github.com/Yugz29/holbertonschool-hbnb.git
cd holbertonschool-hbnb/
```

### **2. Create a Virtual Environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### **3. Install Dependencies**

```bash
pip install -r requirements.txt
```

### **4. Configure the Database**

Ensure you have a supported relational database installed (e.g., PostgreSQL, MySQL, or SQLite).  
Update the `SQLALCHEMY_DATABASE_URI` in `config.py` with your database connection string.

### **5. Run Database Migrations**

Apply database migrations or execute the provided SQL scripts in the `sql/` directory to create the schema.

### **6. Run the Application**

```bash
python run.py
```

The application will start locally at:
```
http://127.0.0.1:5000/
```

You can access the API documentation at:
```
http://127.0.0.1:5000/api/v1/
```

---

## 🔐 Authentication and Authorization

- **JWT Authentication:**  
  Users authenticate by obtaining a JSON Web Token (JWT) via login endpoints. Tokens must be included in the `Authorization` header for protected routes.

- **Role-Based Access Control (RBAC):**  
  User roles (e.g., admin, user) determine access rights to various API endpoints and operations. Roles are enforced in the API layer to protect resources and actions.

---

## 🧱 Key Files

| File | Description |
|------|--------------|
| `run.py` | Entry point to start the Flask application. |
| `config.py` | Environment and database configuration, including JWT settings. |
| `repository.py` | Implements the SQLAlchemy-based repository for data persistence. |
| `facade.py` | Coordinates business logic between API, models, and persistence layers using the Facade pattern. |
| `app/api/v1/*.py` | REST API endpoints implementing authentication, authorization, and CRUD operations for domain models. |
| `tests/` | Unit and integration tests covering authentication, authorization, and CRUD functionality. |

---

## 📚 Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Flask-JWT-Extended Documentation](https://flask-jwt-extended.readthedocs.io/)
- [Flask-RESTx Documentation](https://flask-restx.readthedocs.io/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Role-Based Access Control (RBAC) Concepts](https://auth0.com/docs/authorization/rbac)
- [Facade Design Pattern in Python](https://refactoring.guru/design-patterns/facade/python/example)

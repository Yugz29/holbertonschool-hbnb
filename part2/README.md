# 🏠 HBnB part2

## Overview

The **HBnB API** is a modular Flask-based web application designed to manage core components of the HBnB platform — such as **users**, **places**, **reviews**, and **amenities**.  
This project follows a **three-layer architecture**:  
- **Presentation Layer (API)** — Handles HTTP requests and responses.  
- **Business Logic Layer (Services)** — Manages the core logic through the **Facade pattern**.  
- **Persistence Layer (Repository)** — Handles object storage using an **in-memory repository**, to be replaced by a database later.

This architecture ensures scalability, maintainability, and clear separation of concerns.

---

## 📁 Project Structure

```
hbnb/
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
├── run.py
├── config.py
├── requirements.txt
├── README.md
```

---

## 🧩 Layers Description

### **1. Presentation Layer (API)**
Located under `app/api/v1/`, this layer contains the REST endpoints that expose application functionalities to clients.

### **2. Business Logic Layer (Services)**
Implemented in `app/services/facade.py`, the **Facade pattern** centralizes communication between API routes, models, and repositories.  
This ensures that the logic remains consistent and easy to extend.

### **3. Persistence Layer (Repository)**
Located in `app/persistence/repository.py`, this layer temporarily uses an **in-memory repository** to store and retrieve data objects.  
It will later be replaced by a **database-backed repository** using SQLAlchemy.

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

### **4. Run the Application**

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

## 🧱 Key Files

| File | Description |
|------|--------------|
| `run.py` | Entry point to start the Flask application. |
| `config.py` | Environment configuration file. |
| `repository.py` | Contains the abstract repository and in-memory implementation. |
| `facade.py` | Implements the Facade pattern for managing communication between layers. |

---

## 🧠 Future Improvements

- Replace the in-memory repository with **SQLAlchemy**.
- Add **CRUD operations** for users, places, reviews, and amenities.
- Implement **authentication** and **authorization**.
- Integrate **testing suite** with `pytest`.
- Add **CI/CD pipeline** for automated deployment.

---

## 📚 Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Flask-RESTx Documentation](https://flask-restx.readthedocs.io/)
- [Python Project Structure Best Practices](https://realpython.com/python-application-layouts/)
- [Facade Design Pattern in Python](https://refactoring.guru/design-patterns/facade/python/example)

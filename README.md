# 🏠 HBnB Evolution

HBnB Evolution is a simplified version of AirBnB, developed as an educational project to explore full-stack development, object-oriented architecture, and API design.

---

## 📍 Project Objective

The main goal of HBnB Evolution is to provide a **modular and robust booking platform**, where users can:

* Register and manage their profile (regular user or administrator)
* Create and manage properties (places) with title, description, price, and location
* Add and manage amenities
* Submit and view reviews

---

## Part 1: Technical Documentation  ✅

The first phase of the project focuses on **UML documentation** and the overall application structure. It includes:

* A **package diagram** showing the three main layers: presentation, business logic, and persistence
* A **class diagram** detailing the main entities: `User`, `Place`, `Amenity`, `Review`, and `BaseModel`, along with their attributes and methods
* **Sequence diagrams** illustrating key interactions between layers for primary API calls: user registration, place creation, review submission, fetching the list of places

> This documentation provides a **clear blueprint** for the development process.

---

## Part 2: Backend API and Testing  ✅

The second phase delivers a fully functional backend API with comprehensive validation and unit testing. Key features include:

* RESTful API endpoints for all entities supporting CRUD operations
* Input validation and error handling to ensure data integrity
* A facade layer abstracting business logic for cleaner architecture
* Extensive unit tests covering models, views, and controllers

---

## Part 3: Enhanced Backend with Authentication and Database Integration  ✅

The third phase focuses on strengthening the backend by integrating secure authentication mechanisms and robust database support. This phase aims to enhance security, data consistency, and scalability of the HBnB platform.

Key features include:

* Implementation of user authentication using token-based methods (e.g., JWT) to secure API endpoints
* Role-based access control to differentiate permissions between regular users and administrators
* Integration with a relational database management system (e.g., MySQL, PostgreSQL) for persistent data storage
* Database schema design and migration scripts to support entities and relationships
* Optimization of data retrieval with indexing and query tuning
* Enhanced error handling to manage authentication failures and database exceptions
* Additional unit and integration tests covering authentication workflows and database operations

> This phase ensures a **secure and scalable backend foundation**, ready for production deployment and further frontend integration.

---

### Part 4: Frontend Development with Modular Architecture 🚧

The fourth phase delivers a modern, responsive web interface with modular JavaScript architecture. Key features include:

* **Authentication Pages**: Login and registration forms with JWT token management
* **Main Application Interface**: Interactive place listings with filtering capabilities
* **Place Details**: Dynamic content loading with reviews and amenities display
* **Modular Architecture**: Separation of concerns with dedicated scripts for authentication, places, and reviews
* **Responsive Design**: Mobile-first approach ensuring compatibility across devices
* **Security Integration**: Cookie-based authentication with HttpOnly flags
* **Error Handling**: User-friendly error messages and loading states

> This phase provides a **complete user-facing application** ready for real-world usage.

---

## Project Structure

* `part1/` : UML documentation and diagrams for Part 1
* `part2/` : Backend API implementation, validation, and testing
* `part3/` : Authentication, database integration, and security enhancements
* `part4/` : Frontend application with modular JavaScript architecture


---

## 🔜 Next Steps

* Deployment and scalability improvements

---

> **Note**: This project is currently under development. Documentation and code are evolving throughout the project stages.

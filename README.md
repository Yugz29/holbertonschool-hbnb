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

## Project Structure

* `part1/` : UML documentation and diagrams for Part 1
* `part2/` : Backend API implementation, validation, and testing

---

## 🔜 Next Steps

* Integration with a database for data persistence
* Frontend development and API consumption
* Deployment and scalability improvements

---

> **Note**: This project is currently under development. Documentation and code are evolving throughout the project stages.

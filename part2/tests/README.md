# 🏠 HBnB API - Test Report

## Objective
Verify the functioning of the `User`, `Place`, `Review`, and `Amenity` endpoints according to the validations and business rules defined in the project.

---

## 1. User Tests

| Endpoint | Method | Input | Expected Result | Actual Result | Status |
|----------|---------|--------|-----------------|---------------|--------|
| /api/v1/users/ | POST | first_name, last_name, email | 201, JSON with `id` and user data | Compliant | ✅ |
| /api/v1/users/ | POST | empty/invalid values | 400, JSON with `error` | Compliant | ✅ |
| /api/v1/users/{id} | GET | - | 200, JSON with user data | Compliant | ✅ |
| /api/v1/users/nonexistent | GET | - | 404, JSON with `error` | Compliant | ✅ |
| /api/v1/users/{id} | PUT | Valid modification | 200, JSON with modified data | Compliant | ✅ |
| /api/v1/users/{id} | PUT | Invalid data | 400, JSON with `error` | Compliant | ✅ |
| /api/v1/users/nonexistent | PUT | - | 404, JSON with `error` | Compliant | ✅ |
| /api/v1/users/{id} | DELETE | - | 200, user deleted | Compliant | ✅ |
| /api/v1/users/nonexistent | DELETE | - | 404, JSON with `error` | Compliant | ✅ |

---

## 2. Place Tests

| Endpoint | Method | Input | Expected Result | Actual Result | Status |
|----------|---------|--------|-----------------|---------------|--------|
| /api/v1/places/ | POST | Valid data with `owner_id` | 201, JSON with `id` | Compliant | ✅ |
| /api/v1/places/ | POST | Invalid data (empty title, latitude > 90, etc.) | 400, JSON with `error` | Compliant | ✅ |
| /api/v1/places/{id} | GET | - | 200, JSON with place data | Compliant | ✅ |
| /api/v1/places/nonexistent | GET | - | 404, JSON with `error` | Compliant | ✅ |
| /api/v1/places/{id} | PUT | Valid data | 200, JSON with modified data | Compliant | ✅ |
| /api/v1/places/{id} | PUT | Invalid data | 400, JSON with `error` | Compliant | ✅ |
| /api/v1/places/nonexistent | PUT | - | 404, JSON with `error` | Compliant | ✅ |
| /api/v1/places/{id} | DELETE | - | 200, place deleted | Compliant | ✅ |
| /api/v1/places/nonexistent | DELETE | - | 404, JSON with `error` | Compliant | ✅ |

---

## 3. Review Tests

| Endpoint | Method | Input | Expected Result | Actual Result | Status |
|----------|---------|--------|-----------------|---------------|--------|
| /api/v1/reviews/ | POST | Valid data | 201, JSON with `id`, `text`, `rating`, `user_id`, `place_id` | Compliant | ✅ |
| /api/v1/reviews/ | POST | Invalid data (empty text, rating out of bounds) | 400, JSON with `error` | Compliant | ✅ |
| /api/v1/reviews/{id} | GET | - | 200, JSON with review data | Compliant | ✅ |
| /api/v1/reviews/nonexistent | GET | - | 404, JSON with `error` | Compliant | ✅ |
| /api/v1/reviews/{id} | PUT | Valid data | 200, JSON with `message: Review updated successfully` | Compliant | ✅ |
| /api/v1/reviews/{id} | PUT | Invalid data | 400, JSON with `error` | Compliant | ✅ |
| /api/v1/reviews/{id} | DELETE | - | 200, JSON with `message: Review deleted successfully` | Compliant | ✅ |
| /api/v1/reviews/nonexistent | DELETE | - | 404, JSON with `error` | Compliant | ✅ |

---

## 4. Amenity Tests

| Endpoint | Method | Input | Expected Result | Actual Result | Status |
|----------|---------|--------|-----------------|---------------|--------|
| /api/v1/amenities/ | POST | `{"name":"WiFi"}` | 201, JSON with `id` and `name` | Compliant | ✅ |
| /api/v1/amenities/ | POST | `{"name":""}` | 400, JSON with `error` | Compliant | ✅ |
| /api/v1/amenities/{id} | GET | - | 200, JSON with `id` and `name` | Compliant | ✅ |
| /api/v1/amenities/nonexistent | GET | - | 404, JSON with `error` | Compliant | ✅ |
| /api/v1/amenities/{id} | PUT | Valid data | 200, JSON with modified `id` and `name` | Compliant | ✅ |
| /api/v1/amenities/{id} | PUT | Invalid data | 400, JSON with `error` | Compliant | ✅ |
| /api/v1/amenities/{id} | DELETE | - | 200, deleted | Compliant | ✅ |
| /api/v1/amenities/nonexistent | DELETE | - | 404, JSON with `error` | Compliant | ✅ |

---

## Observations

- All automated unit tests pass.
- Business validations (required fields, limits, valid references) are properly tested.
- Endpoints return appropriate HTTP codes and clear error messages.
- Tests cover positive and negative cases.

---

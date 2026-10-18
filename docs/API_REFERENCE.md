<<<<<<< HEAD
# API reference

The running FastAPI service generates the detailed, current schemas and endpoint descriptions:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- OpenAPI JSON: `http://localhost:8000/openapi.json`

These routes are available when running `backend/main.py`. The API uses JSON requests and responses except where an endpoint accepts an uploaded avatar file. Protected operations use a JWT access token in `Authorization: Bearer <token>`.

## Route groups

| Prefix | Functionality |
| --- | --- |
| `/auth` | Register with email/mobile, log in, use optional Google/GitHub sign-in, request/confirm password reset, read the authenticated user, and change password |
| `/users` | Profile read/update and avatar upload |
| `/vehicles` | Create, list, update, and delete vehicles |
| `/rides` | Create, list/search, update, and manage ride lifecycle; includes QR-token generation and verification endpoints |
| `/bookings` | Request a booking, list passenger/ride bookings, confirm, cancel, and waitlist operations |
| `/ratings` | Create/read/update/delete ratings and find rating candidates |
| `/notifications` | Read and update the current user's in-app notifications |
| `/sos` | Create and view the current user's safety event records |
| `/admin` | Admin-only management, reports, and SOS triage |
| `/payments` | Participant/admin reads, driver/passenger history, earnings, and admin status tracking |

The health endpoint is `GET /health`; it confirms the API process responds, not that PostgreSQL is reachable. Registration requires a valid 10-digit Indian mobile number and accepts driver and passenger roles. Administrative routes require an already provisioned admin account; public registration does not create one. Password reset requires SMTP configuration; reset requests return a generic response for unknown accounts. Social sign-in is optional and requires provider credentials and an existing account with a matching verified email.

Password reset endpoints:

- `POST /auth/password-reset/request` with `{ "email": "..." }` sends a one-time link when SMTP is configured.
- `POST /auth/password-reset/confirm` with `{ "token": "...", "new_password": "..." }` consumes the token once before it expires.

For implementation details, see `backend/app/api/routes` and the relevant service and schema modules. This summary intentionally does not duplicate the generated OpenAPI endpoint list.
=======
# 📡 CommuteShare API Reference

Complete API reference for the **CommuteShare Backend**.

CommuteShare provides a REST API for managing authentication, users, vehicles, rides, bookings, ratings, notifications, SOS events, payments, and administrative operations.

---

## 📋 Table of Contents

* [Base URL](#-base-url)
* [Interactive API Documentation](#-interactive-api-documentation)
* [Authentication](#-authentication)
* [User Roles](#-user-roles)
* [Response Codes](#-response-codes)
* [Health & Root](#-health--root)
* [Authentication Endpoints](#-authentication-endpoints)
* [User Endpoints](#-user-endpoints)
* [Vehicle Endpoints](#-vehicle-endpoints)
* [Ride Endpoints](#-ride-endpoints)
* [Booking Endpoints](#-booking-endpoints)
* [Rating Endpoints](#-rating-endpoints)
* [Notification Endpoints](#-notification-endpoints)
* [SOS Endpoints](#-sos-endpoints)
* [Payment Endpoints](#-payment-endpoints)
* [Admin Endpoints](#-admin-endpoints)

---

# 🌐 Base URL

When running locally:

```text
http://localhost:8000
```

All endpoints are relative to this URL.

Example:

```text
http://localhost:8000/auth/login
```

---

# 📖 Interactive API Documentation

FastAPI automatically provides interactive API documentation.

| Documentation | URL      |
| ------------- | -------- |
| Swagger UI    | `/docs`  |
| ReDoc         | `/redoc` |

Local URLs:

```text
http://localhost:8000/docs
```

```text
http://localhost:8000/redoc
```

Swagger UI is recommended for testing endpoints directly.

---

# 🔐 Authentication

CommuteShare uses JWT-based authentication.

After a successful login, the API returns an access token:

```json
{
  "message": "Login successful",
  "access_token": "your_jwt_access_token",
  "token_type": "bearer"
}
```

For protected endpoints, include the token in the request header:

```http
Authorization: Bearer <access_token>
```

---

# 👥 User Roles

CommuteShare supports three main roles.

| Role        | Description                                                                     |
| ----------- | ------------------------------------------------------------------------------- |
| `PASSENGER` | Can search, book, confirm rides, rate users, and manage personal bookings       |
| `DRIVER`    | Can register vehicles, create rides, manage bookings, and manage ride lifecycle |
| `ADMIN`     | Can access administrative statistics and platform management endpoints          |

---

# 🚦 Response Codes

| Code                        | Meaning                                              |
| --------------------------- | ---------------------------------------------------- |
| `200 OK`                    | Request completed successfully                       |
| `201 Created`               | Resource created successfully                        |
| `204 No Content`            | Request completed successfully with no response body |
| `400 Bad Request`           | Invalid request or business rule violation           |
| `401 Unauthorized`          | Authentication required or token invalid             |
| `403 Forbidden`             | User does not have permission                        |
| `404 Not Found`             | Requested resource does not exist                    |
| `422 Unprocessable Entity`  | Request validation failed                            |
| `500 Internal Server Error` | Unexpected server error                              |

---

# ❤️ Health & Root

## Health Check

```http
GET /health
```

### Response

```json
{
  "status": "healthy",
  "service": "CommuteShare Backend"
}
```

---

## Root Endpoint

```http
GET /
```

### Response

```json
{
  "message": "Welcome to CommuteShare API",
  "version": "1.0.0",
  "docs": "/docs"
}
```

---

# 🔐 Authentication Endpoints

Base path:

```text
/auth
```

---

## Register User

Creates a new CommuteShare account.

```http
POST /auth/register
```

### Request Body

```json
{
  "full_name": "John Doe",
  "email": "john@example.com",
  "phone_number": "9876543210",
  "bio": "Daily commuter",
  "profile_image": null,
  "role": "PASSENGER",
  "password": "SecurePassword123"
}
```

### Roles

```text
PASSENGER
DRIVER
```

### Success Response

```http
201 Created
```

The API returns the created user.

---

## Login

Authenticates a user and returns a JWT access token.

```http
POST /auth/login
```

> This endpoint uses OAuth2 form data.

### Request Body

```text
username=john@example.com
password=SecurePassword123
```

### Response

```json
{
  "message": "Login successful",
  "access_token": "eyJhbGciOi...",
  "token_type": "bearer"
}
```

---

## Get Current User

Returns the currently authenticated user.

```http
GET /auth/me
```

### Authentication

```text
Required
```

---

## Change Password

Changes the password of the authenticated user.

```http
PUT /auth/change-password
```

### Request Body

```json
{
  "current_password": "OldPassword123",
  "new_password": "NewPassword123"
}
```

### Response

```http
204 No Content
```

---

# 👤 User Endpoints

Base path:

```text
/users
```

---

## Get Current User Profile

```http
GET /users/me
```

### Authentication

```text
Required
```

---

## Get User by ID

```http
GET /users/{user_id}
```

### Example

```http
GET /users/12
```

---

## Update Current User Profile

```http
PUT /users/me
```

### Request Body

All fields are optional.

```json
{
  "full_name": "John Doe",
  "phone_number": "9876543210",
  "bio": "Cybersecurity student and daily commuter",
  "profile_image": null
}
```

---

## Deactivate Current Account

Deactivates the authenticated user's account.

```http
DELETE /users/me
```

### Response

```http
204 No Content
```

---

# 🚙 Vehicle Endpoints

Base path:

```text
/vehicles
```

---

## Register Vehicle

Registers a new vehicle.

```http
POST /vehicles/
```

### Authentication

```text
Driver Required
```

### Request Body

```json
{
  "make": "Honda",
  "model": "City",
  "color": "White",
  "registration_number": "KA20AB1234",
  "seating_capacity": 4
}
```

### Success Response

```http
201 Created
```

---

## Get My Vehicles

Returns all vehicles owned by the authenticated user.

```http
GET /vehicles/
```

### Authentication

```text
Required
```

---

## Get Vehicle

```http
GET /vehicles/{vehicle_id}
```

### Example

```http
GET /vehicles/5
```

---

## Update Vehicle

```http
PUT /vehicles/{vehicle_id}
```

### Authentication

```text
Driver Required
```

### Request Body

```json
{
  "make": "Honda",
  "model": "City",
  "color": "Black",
  "seating_capacity": 4,
  "is_active": true
}
```

All fields are optional.

---

## Delete Vehicle

```http
DELETE /vehicles/{vehicle_id}
```

### Authentication

```text
Driver Required
```

### Response

```http
204 No Content
```

---

# 🚗 Ride Endpoints

Base path:

```text
/rides
```

---

## Create Ride

Creates a new ride.

```http
POST /rides/
```

### Authentication

```text
Driver Required
```

### Request Body

```json
{
  "vehicle_id": 1,
  "pickup_location": "Nitte",
  "pickup_latitude": 13.178,
  "pickup_longitude": 74.934,
  "destination_location": "Mangalore",
  "destination_latitude": 12.914,
  "destination_longitude": 74.856,
  "departure_time": "2026-08-25T08:00:00",
  "estimated_arrival_time": "2026-08-25T10:00:00",
  "total_seats": 3,
  "price_per_seat": 150,
  "notes": "Leaving from college campus"
}
```

### Success Response

```http
201 Created
```

---

## Get Available Rides

Returns available rides.

```http
GET /rides/
```

### Authentication

```text
Not Required
```

---

## Get Ride Details

```http
GET /rides/{ride_id}
```

### Example

```http
GET /rides/10
```

---

## Search Rides

Searches for rides using source and destination.

```http
GET /rides/search/?source={source}&destination={destination}
```

### Example

```http
GET /rides/search/?source=Nitte&destination=Mangalore
```

---

## Update Ride

Updates a ride owned by the authenticated driver.

```http
PUT /rides/{ride_id}
```

### Authentication

```text
Driver Required
```

### Request Body

All fields are optional.

```json
{
  "pickup_location": "Nitte",
  "destination_location": "Mangalore",
  "departure_time": "2026-08-25T09:00:00",
  "total_seats": 3,
  "price_per_seat": 180,
  "notes": "Updated departure time"
}
```

---

## Delete Ride

Deletes a ride owned by the authenticated driver.

```http
DELETE /rides/{ride_id}
```

### Authentication

```text
Driver Required
```

### Response

```http
204 No Content
```

---

## Start Ride

Starts a ride.

```http
PATCH /rides/{ride_id}/start
```

### Authentication

```text
Driver Required
```

---

## End Ride

Marks a ride as completed.

```http
PATCH /rides/{ride_id}/end
```

### Authentication

```text
Driver Required
```

---

## Confirm Ride

Allows a passenger to confirm a ride.

```http
PATCH /rides/{ride_id}/confirm
```

### Authentication

```text
Passenger Required
```

---

# 📱 QR Boarding

## Generate Boarding QR Token

Generates a QR boarding token for a ride.

```http
POST /rides/{ride_id}/generate-qr
```

### Authentication

```text
Driver Required
```

The driver must own the ride.

### Response

```json
{
  "qr_token": "generated_token"
}
```

---

## Verify Boarding QR

Verifies a passenger boarding QR token.

```http
POST /rides/verify-boarding
```

### Authentication

```text
Passenger Required
```

### Request Body

```json
{
  "qr_token": "generated_token"
}
```

---

# 📅 Booking Endpoints

Base path:

```text
/bookings
```

---

## Book a Ride

Creates a booking for a ride.

```http
POST /bookings/
```

### Authentication

```text
Required
```

### Request Body

```json
{
  "ride_id": 10
}
```

### Success Response

```http
201 Created
```

---

## Get My Bookings

Returns bookings belonging to the authenticated user.

```http
GET /bookings/me
```

### Authentication

```text
Required
```

---

## Get Booking Statistics

Returns statistics related to the authenticated user's bookings.

```http
GET /bookings/me/statistics
```

### Authentication

```text
Required
```

---

## Get Ride Bookings

Returns bookings for a specific ride.

```http
GET /bookings/ride/{ride_id}
```

### Authentication

```text
Driver Required
```

The authenticated driver must own the ride.

---

## Confirm Booking

Confirms a booking.

```http
PATCH /bookings/{booking_id}/confirm
```

### Authentication

```text
Driver Required
```

The authenticated driver must own the ride associated with the booking.

---

## Cancel Booking

Cancels a booking.

```http
DELETE /bookings/{booking_id}
```

### Authentication

```text
Required
```

Only the passenger who owns the booking can cancel it.

### Response

```http
204 No Content
```

---

# ⭐ Rating Endpoints

Base path:

```text
/ratings
```

---

## Create Rating

Creates a rating after an eligible ride or booking.

```http
POST /ratings/
```

### Authentication

```text
Required
```

### Request Body

```json
{
  "booking_id": 10,
  "rating": 5,
  "review": "Great ride and a very friendly driver."
}
```

### Rating Range

```text
1 – 5
```

---

## Get My Ratings

Returns ratings associated with the authenticated user.

```http
GET /ratings/me
```

### Authentication

```text
Required
```

---

## Get Rating Candidates

Returns users who are eligible to be rated.

```http
GET /ratings/candidates
```

### Authentication

```text
Required
```

---

## Get Ratings for User

```http
GET /ratings/user/{user_id}
```

### Example

```http
GET /ratings/user/12
```

---

## Update Rating

Updates a rating created by the authenticated user.

```http
PUT /ratings/{rating_id}
```

### Request Body

```json
{
  "rating": 4,
  "review": "Good ride overall."
}
```

All fields are optional.

---

## Delete Rating

Deletes a rating created by the authenticated user.

```http
DELETE /ratings/{rating_id}
```

### Response

```http
204 No Content
```

---

# 🔔 Notification Endpoints

Base path:

```text
/notifications
```

All notification endpoints require authentication.

---

## Get All Notifications

```http
GET /notifications/
```

---

## Get Unread Notifications

```http
GET /notifications/unread
```

---

## Mark Notification as Read

```http
PATCH /notifications/{notification_id}/read
```

The notification must belong to the authenticated user.

---

## Mark All Notifications as Read

```http
PATCH /notifications/read-all
```

### Response

```json
{
  "message": "All notifications marked as read."
}
```

---

# 🆘 SOS Endpoints

Base path:

```text
/sos
```

---

## Trigger SOS

Creates an SOS emergency event.

```http
POST /sos/
```

### Authentication

```text
Required
```

### Request Body

```json
{
  "ride_id": 10,
  "emergency_type": "Medical Emergency",
  "description": "Passenger requires immediate assistance.",
  "latitude": 13.178,
  "longitude": 74.934
}
```

### Success Response

```http
201 Created
```

---

## Get My SOS History

Returns SOS events created by the authenticated user.

```http
GET /sos/me
```

### Authentication

```text
Required
```

---

## Get SOS Event

Returns details of an SOS event.

```http
GET /sos/{sos_id}
```

### Authentication

```text
Required
```

Users can only access their own SOS events.

---

# 💳 Payment Endpoints

Base path:

```text
/payments
```

---

## Get Payment

```http
GET /payments/{payment_id}
```

### Authentication

```text
Required
```

---

## Get Payment for Booking

```http
GET /payments/booking/{booking_id}
```

### Authentication

```text
Required
```

---

## Mark Payment as Paid

```http
PATCH /payments/{payment_id}/paid
```

### Authentication

```text
Required
```

### Request Body

```json
{
  "method": "UPI"
}
```

---

## Mark Payment as Failed

```http
PATCH /payments/{payment_id}/failed
```

### Authentication

```text
Required
```

---

## Driver Payment History

```http
GET /payments/driver/history
```

### Authentication

```text
Driver Required
```

---

## Passenger Payment History

```http
GET /payments/passenger/history
```

### Authentication

```text
Passenger Required
```

---

## Driver Earnings

Returns driver earnings.

```http
GET /payments/driver/earnings
```

### Authentication

```text
Driver Required
```

### Response

```json
{
  "completed_payments": 10,
  "total_earnings": 2500
}
```

---

## Platform Revenue

Returns overall platform revenue statistics.

```http
GET /payments/admin/revenue
```

### Authentication

```text
Admin Required
```

### Response

```json
{
  "paid_payments": 100,
  "total_revenue": 25000
}
```

---

# 👨‍💼 Admin Endpoints

Base path:

```text
/admin
```

> All admin endpoints require administrator privileges.

---

## Dashboard Statistics

```http
GET /admin/dashboard
```

Returns platform-level statistics.

---

## Get All Users

```http
GET /admin/users
```

---

## Activate User

```http
PATCH /admin/users/{user_id}/activate
```

---

## Deactivate User

```http
PATCH /admin/users/{user_id}/deactivate
```

---

## Get All Rides

```http
GET /admin/rides
```

---

## Get All Bookings

```http
GET /admin/bookings
```

---

# 🔄 Typical API Workflow

## Passenger Workflow

```text
Register
   ↓
Login
   ↓
Search Available Rides
   ↓
Book Ride
   ↓
Confirm Ride
   ↓
Complete Journey
   ↓
Make Payment
   ↓
Rate Driver
```

---

## Driver Workflow

```text
Register as Driver
   ↓
Login
   ↓
Register Vehicle
   ↓
Create Ride
   ↓
Receive Booking Requests
   ↓
Confirm Bookings
   ↓
Start Ride
   ↓
End Ride
   ↓
View Earnings
```

---

# 🛡️ Security Notes

CommuteShare protects sensitive API operations using:

* JWT Authentication
* Password Hashing
* Role-Based Access Control
* Ownership Validation
* Pydantic Request Validation
* Protected Administrative Routes
* Environment-Based Configuration
* CORS Configuration

---

# 🧪 Testing the API

The easiest way to test the API locally is through Swagger UI:

```text
http://localhost:8000/docs
```

Recommended testing workflow:

1. Register a user.
2. Login to obtain an access token.
3. Click **Authorize** in Swagger UI.
4. Enter:

```text
Bearer <your_access_token>
```

5. Test protected endpoints.

---

<div align="center">

### 📡 CommuteShare API — Connecting Commuters, One Endpoint at a Time.

</div>
>>>>>>> origin/main

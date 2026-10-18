<<<<<<< HEAD
# Frontend development

The frontend is a React application built with Vite. It uses React Router, Axios, Tailwind CSS, and Leaflet. See the root [README](../README.md) for full application setup and Compose instructions.

## Local setup

```sh
npm ci
npm run dev
```

Vite serves the app at `http://localhost:5173`. The Axios client defaults to `http://127.0.0.1:8000`. To use another API origin, create `.env.local` in this directory:

```dotenv
VITE_API_BASE_URL=http://127.0.0.1:8000
```

The optional `VITE_OSM_TILE_URL` variable changes the Leaflet tile URL. Vite variables are public browser configuration; never place secrets in them. The map displays a straight-line connection and does not provide road routing or travel-time estimates.

## Checks

```sh
npm test
npm run build
```

Tests use Node's built-in test runner (`node --test`). See [API groups](../docs/API_REFERENCE.md) and [known limitations](../docs/ROADMAP.md).
=======
# 🚗 CommuteShare — Frontend

The frontend of **CommuteShare**, a community-driven ride-sharing platform designed to help daily commuters discover rides, manage bookings, and coordinate their journeys through a modern web application.

Built using React and Vite, the frontend communicates with the CommuteShare REST API to provide a responsive interface for riders, drivers, and administrators.

---

## ✨ Features

* 🔐 User Registration & Authentication
* 👤 User Profile Management
* 🚗 Browse Available Rides
* ➕ Create and Manage Rides
* 📅 Ride Booking Management
* 🚙 Vehicle Management
* ⭐ Driver and Ride Ratings
* 🔔 Notifications
* 🆘 SOS Emergency Reporting
* 👨‍💼 Admin Dashboard
* 🛡️ Role-Based Access Control
* 🗺️ Map Integration with Leaflet
* 📊 Data Visualization and Dashboard Components
* 🔄 API Integration with Axios
* 🔒 Protected Routes

---

## 🛠️ Tech Stack

| Technology      | Purpose                  |
| --------------- | ------------------------ |
| React 19        | Frontend UI              |
| Vite            | Development & Build Tool |
| React Router    | Client-Side Routing      |
| Axios           | API Communication        |
| React Hook Form | Form Management          |
| React Hot Toast | Notifications            |
| Leaflet         | Map Functionality        |
| React Leaflet   | React Map Components     |
| Recharts        | Data Visualization       |
| Lucide React    | Icons                    |
| Tailwind CSS    | Styling                  |

---

## 📁 Project Structure

```text
frontend/
│
├── public/
│   └── favicon.ico
│
├── src/
│   ├── api/
│   │   ├── admin.js
│   │   ├── auth.js
│   │   ├── axios.js
│   │   ├── bookings.js
│   │   ├── notifications.js
│   │   ├── ratings.js
│   │   ├── rides.js
│   │   ├── sos.js
│   │   ├── users.js
│   │   └── vehicles.js
│   │
│   ├── assets/
│   │   └── logo.svg
│   │
│   ├── components/
│   │
│   ├── constants/
│   │   ├── roles.js
│   │   └── routes.js
│   │
│   ├── context/
│   │   └── AuthContext.jsx
│   │
│   ├── hooks/
│   │   ├── useAdmin.js
│   │   ├── useAuth.js
│   │   ├── useBookings.js
│   │   ├── useNotifications.js
│   │   ├── useRatings.js
│   │   ├── useRides.js
│   │   ├── useSOS.js
│   │   └── useVehicles.js
│   │
│   ├── pages/
│   │   ├── LoginPage.jsx
│   │   ├── RegisterPage.jsx
│   │   ├── DashboardPage.jsx
│   │   ├── AdminDashboardPage.jsx
│   │   ├── RidesPage.jsx
│   │   ├── RideDetailsPage.jsx
│   │   ├── BookingsPage.jsx
│   │   ├── VehiclesPage.jsx
│   │   ├── ProfilePage.jsx
│   │   ├── RatingsPage.jsx
│   │   ├── NotificationsPage.jsx
│   │   ├── SOSPage.jsx
│   │   ├── 403Page.jsx
│   │   └── NotFoundPage.jsx
│   │
│   ├── routes/
│   │   └── AppRoutes.jsx
│   │
│   ├── store/
│   │   └── authStore.js
│   │
│   ├── utils/
│   │   ├── date.js
│   │   ├── formatCurrency.js
│   │   ├── storage.js
│   │   └── validators.js
│   │
│   ├── App.jsx
│   ├── main.jsx
│   └── index.css
│
├── Dockerfile
├── index.html
├── package.json
├── vite.config.js
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

Make sure you have the following installed:

* Node.js
* npm
* CommuteShare Backend running locally

---

### 1. Navigate to the Frontend

```bash
cd frontend
```

### 2. Install Dependencies

```bash
npm install
```

### 3. Configure Environment Variables

Create a `.env` file if required for your local API configuration.

Example:

```env
VITE_API_BASE_URL=http://localhost:8000
```

### 4. Start the Development Server

```bash
npm run dev
```

The application will typically be available at:

```text
http://localhost:5173
```

---

## 📜 Available Scripts

### Start Development Server

```bash
npm run dev
```

### Build for Production

```bash
npm run build
```

### Preview Production Build

```bash
npm run preview
```

---

## 🔐 Authentication Flow

CommuteShare uses token-based authentication.

```text
User
  │
  ▼
Login / Register
  │
  ▼
Authentication API
  │
  ▼
Access Token
  │
  ▼
Stored Authentication State
  │
  ▼
Protected Routes
```

The frontend uses:

* Authentication Context
* Custom Authentication Hooks
* Protected Routes
* Role-Based Access Control

---

## 👥 User Roles

The application supports different user roles and permissions.

### 👤 User

Regular users can:

* Browse rides
* Book rides
* Manage bookings
* Manage profile information
* Manage vehicles
* Rate rides and users
* Receive notifications
* Report SOS events

### 🚗 Driver

Drivers can:

* Create rides
* Manage their rides
* Manage vehicle information
* View booking requests
* Track ride-related activity

### 👨‍💼 Administrator

Administrators can:

* Access the admin dashboard
* Manage platform activity
* Review users and rides
* Monitor system data

---

## 🌐 API Integration

The frontend communicates with the FastAPI backend through organized API modules.

```text
src/api/
│
├── auth.js
├── users.js
├── rides.js
├── bookings.js
├── vehicles.js
├── ratings.js
├── notifications.js
├── sos.js
└── admin.js
```

Axios is used for HTTP communication and centralized API configuration.

---

## 🐳 Running with Docker

From the project root:

```bash
docker compose up --build
```

This starts:

* PostgreSQL
* FastAPI Backend
* React Frontend

Frontend:

```text
http://localhost:5173
```

Backend:

```text
http://localhost:8000
```

API Documentation:

```text
http://localhost:8000/docs
```

---

## 🧪 Future Improvements

Potential improvements include:

* Real-time ride updates
* Live driver location tracking
* Advanced route optimization
* Mobile application
* Push notifications
* Enhanced analytics
* Improved accessibility
* Dark mode
* Progressive Web App support

---

## 🤝 Contributing

Contributions, improvements, and suggestions are welcome.

1. Fork the repository
2. Create a new branch

```bash
git checkout -b feature/your-feature
```

3. Commit your changes

```bash
git commit -m "Add your feature"
```

4. Push your branch

```bash
git push origin feature/your-feature
```

5. Open a Pull Request

---

## 👨‍💻 Authors

* **Sakshat S**
* **Swasthi Kunder**
* **Neha S**

### 🔗 GitHub

* Sakshat: https://github.com/Sakshats993
* Swasthi: https://github.com/swasthikunder
* Neha: https://github.com/Neha-61

---

<div align="center">

### 🚗 Built to Learn. Built to Break. Built Again. Built Better.

**If you found this project interesting, consider giving the repository a ⭐**

</div>
>>>>>>> origin/main

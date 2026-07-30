
```
CommuteShare
├─ backend
│  ├─ alembic
│  │  ├─ env.py
│  │  ├─ script.py.mako
│  │  └─ versions
│  │     └─ 4ec21e7c4e37_initial_migration.py
│  ├─ alembic.ini
│  ├─ app
│  │  ├─ api
│  │  │  ├─ routes
│  │  │  │  ├─ admin.py
│  │  │  │  ├─ auth.py
│  │  │  │  ├─ bookings.py
│  │  │  │  ├─ notifications.py
│  │  │  │  ├─ ratings.py
│  │  │  │  ├─ rides.py
│  │  │  │  ├─ sos.py
│  │  │  │  ├─ users.py
│  │  │  │  ├─ vehicles.py
│  │  │  │  └─ __init__.py
│  │  │  └─ __init__.py
│  │  ├─ core
│  │  │  ├─ config.py
│  │  │  ├─ deps.py
│  │  │  ├─ exceptions.py
│  │  │  └─ security.py
│  │  ├─ database
│  │  │  ├─ base.py
│  │  │  ├─ session.py
│  │  │  └─ __init__.py
│  │  ├─ models
│  │  │  ├─ audit_log.py
│  │  │  ├─ base_model.py
│  │  │  ├─ booking.py
│  │  │  ├─ enums.py
│  │  │  ├─ notification.py
│  │  │  ├─ rating.py
│  │  │  ├─ ride.py
│  │  │  ├─ sos_event.py
│  │  │  ├─ user.py
│  │  │  ├─ vehicle.py
│  │  │  ├─ waitlist.py
│  │  │  └─ __init__.py
│  │  ├─ schemas
│  │  │  ├─ auth.py
│  │  │  ├─ booking.py
│  │  │  ├─ misc.py
│  │  │  ├─ ride.py
│  │  │  ├─ user.py
│  │  │  ├─ vehicle.py
│  │  │  └─ __init__.py
│  │  ├─ services
│  │  │  ├─ admin_service.py
│  │  │  ├─ audit_service.py
│  │  │  ├─ auth_service.py
│  │  │  ├─ booking_service.py
│  │  │  ├─ matching_service.py
│  │  │  ├─ notification_service.py
│  │  │  ├─ rating_service.py
│  │  │  ├─ reputation_service.py
│  │  │  ├─ ride_service.py
│  │  │  ├─ sos_service.py
│  │  │  ├─ user_service.py
│  │  │  ├─ vehicle_service.py
│  │  │  └─ __init__.py
│  │  ├─ utils
│  │  │  ├─ geolocation.py
│  │  │  ├─ logger.py
│  │  │  ├─ validators.py
│  │  │  └─ __init__.py
│  │  └─ __init__.py
│  ├─ Dockerfile
│  ├─ logs
│  ├─ main.py
│  ├─ README.md
│  ├─ requirements.txt
│  └─ tests
│     ├─ conftest.py
│     ├─ test_auth.py
│     ├─ test_bookings.py
│     ├─ test_rides.py
│     └─ __init__.py
├─ docker-compose.yml
├─ docs
│  ├─ API_REFERENCE.md
│  ├─ ARCHITECTURE.md
│  ├─ architecture.png
│  ├─ DATABASE_SCHEMA.md
│  ├─ DEPLOYMENT.md
│  ├─ ER_Diagram.png
│  ├─ ROADMAP.md
│  └─ SECURITY.md
├─ frontend
│  ├─ Dockerfile
│  ├─ index.html
│  ├─ package-lock.json
│  ├─ package.json
│  ├─ public
│  │  └─ favicon.ico
│  ├─ README.md
│  ├─ src
│  │  ├─ api
│  │  │  ├─ admin.js
│  │  │  ├─ auth.js
│  │  │  ├─ axios.js
│  │  │  ├─ bookings.js
│  │  │  ├─ notifications.js
│  │  │  ├─ ratings.js
│  │  │  ├─ rides.js
│  │  │  ├─ sos.js
│  │  │  ├─ users.js
│  │  │  └─ vehicles.js
│  │  ├─ App.jsx
│  │  ├─ assets
│  │  │  ├─ icons
│  │  │  ├─ images
│  │  │  └─ logo.svg
│  │  ├─ components
│  │  │  ├─ admin
│  │  │  │  ├─ AdminStatistics.jsx
│  │  │  │  ├─ BookingsTable.jsx
│  │  │  │  ├─ RidesTable.jsx
│  │  │  │  ├─ StatisticsCard.jsx
│  │  │  │  └─ UsersTable.jsx
│  │  │  ├─ auth
│  │  │  │  ├─ LoginForm.jsx
│  │  │  │  └─ RegisterForm.jsx
│  │  │  ├─ bookings
│  │  │  │  ├─ BookingCard.jsx
│  │  │  │  ├─ BookingList.jsx
│  │  │  │  ├─ BookingStatistics.jsx
│  │  │  │  └─ CancelBookingModal.jsx
│  │  │  ├─ common
│  │  │  │  ├─ Badge.jsx
│  │  │  │  ├─ Button.jsx
│  │  │  │  ├─ Card.jsx
│  │  │  │  ├─ DashboardCard.jsx
│  │  │  │  ├─ Input.jsx
│  │  │  │  └─ Modal.jsx
│  │  │  ├─ layout
│  │  │  │  ├─ Footer.jsx
│  │  │  │  ├─ Navbar.jsx
│  │  │  │  └─ Sidebar.jsx
│  │  │  ├─ map
│  │  │  │  └─ RideMap.jsx
│  │  │  ├─ notifications
│  │  │  │  ├─ NotificationCard.jsx
│  │  │  │  └─ NotificationList.jsx
│  │  │  ├─ ratings
│  │  │  │  ├─ RatingCard.jsx
│  │  │  │  ├─ RatingForm.jsx
│  │  │  │  └─ RatingList.jsx
│  │  │  ├─ rides
│  │  │  │  ├─ DeleteRideModal.jsx
│  │  │  │  ├─ RideCard.jsx
│  │  │  │  ├─ RideFilters.jsx
│  │  │  │  ├─ RideForm.jsx
│  │  │  │  └─ RideList.jsx
│  │  │  ├─ sos
│  │  │  │  ├─ SOSButton.jsx
│  │  │  │  └─ SOSHistory.jsx
│  │  │  ├─ ui
│  │  │  │  ├─ AdminRoute.jsx
│  │  │  │  ├─ DriverRoute.jsx
│  │  │  │  ├─ EmptyState.jsx
│  │  │  │  ├─ ErrorMessage.jsx
│  │  │  │  ├─ Layout.jsx
│  │  │  │  ├─ LoadingSpinner.jsx
│  │  │  │  ├─ ProtectedRoute.jsx
│  │  │  │  ├─ Skeleton.jsx
│  │  │  │  ├─ SOSButton.jsx
│  │  │  │  └─ Toast.jsx
│  │  │  └─ vehicles
│  │  │     ├─ DeleteVehicleModal.jsx
│  │  │     ├─ VehicleCard.jsx
│  │  │     ├─ VehicleForm.jsx
│  │  │     └─ VehicleList.jsx
│  │  ├─ constants
│  │  │  ├─ roles.js
│  │  │  └─ routes.js
│  │  ├─ context
│  │  │  └─ AuthContext.jsx
│  │  ├─ hooks
│  │  │  ├─ useAdmin.js
│  │  │  ├─ useAuth.js
│  │  │  ├─ useBookings.js
│  │  │  ├─ useNotifications.js
│  │  │  ├─ useRatings.js
│  │  │  ├─ useRides.js
│  │  │  ├─ useSOS.js
│  │  │  └─ useVehicles.js
│  │  ├─ index.css
│  │  ├─ main.jsx
│  │  ├─ pages
│  │  │  ├─ 403Page.jsx
│  │  │  ├─ AdminDashboardPage.jsx
│  │  │  ├─ BookingsPage.jsx
│  │  │  ├─ DashboardPage.jsx
│  │  │  ├─ LoginPage.jsx
│  │  │  ├─ NotFoundPage.jsx
│  │  │  ├─ NotificationsPage.jsx
│  │  │  ├─ ProfilePage.jsx
│  │  │  ├─ RatingsPage.jsx
│  │  │  ├─ RegisterPage.jsx
│  │  │  ├─ RideDetailsPage.jsx
│  │  │  ├─ RidesPage.jsx
│  │  │  ├─ SOSPage.jsx
│  │  │  └─ VehiclesPage.jsx
│  │  ├─ routes
│  │  │  └─ AppRoutes.jsx
│  │  ├─ store
│  │  │  └─ authStore.js
│  │  └─ utils
│  │     ├─ date.js
│  │     ├─ formatCurrency.js
│  │     ├─ storage.js
│  │     └─ validators.js
│  ├─ tailwind.config.js
│  └─ vite.config.js
├─ LICENSE
├─ package-lock.json
├─ package.json
├─ README.md
└─ screenshots

```
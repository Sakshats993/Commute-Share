import { Routes, Route, Navigate } from "react-router-dom";

import LoginPage from "../pages/LoginPage";
import RegisterPage from "../pages/RegisterPage";
import DashboardPage from "../pages/DashboardPage";
import RidesPage from "../pages/RidesPage";
import RideDetailsPage from "../pages/RideDetailsPage";
import VehiclesPage from "../pages/VehiclesPage";
import BookingsPage from "../pages/BookingsPage";
import NotificationsPage from "../pages/NotificationsPage";
import RatingsPage from "../pages/RatingsPage";
import SOSPage from "../pages/SOSPage";
import ProfilePage from "../pages/ProfilePage";
import AdminDashboardPage from "../pages/AdminDashboardPage";
import NotFoundPage from "../pages/NotFoundPage";


import ProtectedRoute from "../components/ui/ProtectedRoute";
import AdminRoute from "../components/ui/AdminRoute";
import DriverRoute from "../components/ui/DriverRoute";

export default function AppRoutes() {
    return (
        <Routes>
            <Route
                path="/"
                element={<Navigate to="/dashboard" replace />}
            />

            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />

            <Route
                path="/dashboard"
                element={
                    <ProtectedRoute>
                        <DashboardPage />
                    </ProtectedRoute>
                }
            />

            <Route
                path="/rides"
                element={
                    <ProtectedRoute>
                        <RidesPage />
                    </ProtectedRoute>
                }
            />

            <Route
                path="/rides/:rideId"
                element={
                    <ProtectedRoute>
                        <RideDetailsPage />
                    </ProtectedRoute>
                }
            />

            <Route
                path="/vehicles"
                element={
                    <DriverRoute>
                        <VehiclesPage />
                    </DriverRoute>
                }
            />

            <Route
                path="/bookings"
                element={
                    <ProtectedRoute>
                        <BookingsPage />
                    </ProtectedRoute>
                }
            />

            <Route
                path="/notifications"
                element={
                    <ProtectedRoute>
                        <NotificationsPage />
                    </ProtectedRoute>
                }
            />

            <Route
                path="/ratings/:userId"
                element={
                    <ProtectedRoute>
                        <RatingsPage />
                    </ProtectedRoute>
                }
            />

            <Route
                path="/sos"
                element={
                    <ProtectedRoute>
                        <SOSPage />
                    </ProtectedRoute>
                }
            />

            <Route
                path="/profile"
                element={
                    <ProtectedRoute>
                        <ProfilePage />
                    </ProtectedRoute>
                }
            />

            <Route
                path="/admin"
                element={
                    <AdminRoute>
                        <AdminDashboardPage />
                    </AdminRoute>
                }
            />

            <Route path="*" element={<NotFoundPage />} />
        </Routes>
    );
}
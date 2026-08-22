import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import {
    Calendar,
    Car,
    Leaf,
    MapPin,
    Wallet,
    Bell,
    Star,
} from "lucide-react";

import DashboardCard from "../components/common/DashboardCard";
import Layout from "../components/ui/Layout";

import ROUTES from "../constants/routes";

import useAuth from "../hooks/useAuth";
import useBookings from "../hooks/useBookings";
import useNotifications from "../hooks/useNotifications";
import useRatings from "../hooks/useRatings";
import useRides from "../hooks/useRides";

export default function DashboardPage() {
    const navigate = useNavigate();

    const { user } = useAuth();

    const { rides } = useRides();
    const { bookings } = useBookings();
    const { notifications } = useNotifications();

    const { ratings, loadRatings } = useRatings();

    useEffect(() => {
        if (user?.id) {
            loadRatings(user.id);
        }
    }, [user?.id, loadRatings]);

    const unreadNotifications = notifications.filter(
        (notification) => !notification.is_read
    ).length;

    const averageRating =
        ratings.length > 0
            ? (
                  ratings.reduce(
                      (sum, rating) => sum + rating.score,
                      0
                  ) / ratings.length
              ).toFixed(1)
            : "0.0";

    // Greeting
    const hour = new Date().getHours();

    let greeting = "Good Evening";
    let emoji = "🌙";

    if (hour < 12) {
        greeting = "Good Morning";
        emoji = "☀️";
    } else if (hour < 17) {
        greeting = "Good Afternoon";
        emoji = "🌤";
    }

    // Profile completion
    let profileCompletion = 0;

    if (user?.full_name) profileCompletion += 25;
    if (user?.email) profileCompletion += 25;
    if (user?.phone_number) profileCompletion += 25;
    if (user?.profile_image) profileCompletion += 25;

    // ==========================
    // Recent Activity
    // ==========================

    const recentActivities = [];

    bookings.slice(0, 3).forEach((booking) => {
        recentActivities.push({
            title: "Ride booked successfully",
            time: booking.created_at,
            icon: <Car className="text-green-600" size={18} />,
        });
    });

    notifications.slice(0, 3).forEach((notification) => {
        recentActivities.push({
            title: notification.title,
            time: notification.created_at,
            icon: <Bell className="text-blue-600" size={18} />,
        });
    });

    ratings.slice(0, 2).forEach((rating) => {
        recentActivities.push({
            title: `Received ${rating.score}★ rating`,
            time: rating.created_at,
            icon: <Star className="text-yellow-500" size={18} />,
        });
    });

    recentActivities.sort(
        (a, b) => new Date(b.time) - new Date(a.time)
    );

    return (
        <Layout>
            {/* Greeting */}
            <div className="mb-10">
                <h1 className="text-4xl font-bold text-gray-900">
                    {emoji} {greeting},
                    <span className="ml-2 text-green-600">
                        {user?.full_name}
                    </span>
                </h1>

                <p className="mt-2 text-gray-500">
                    Welcome back! Here's your CommuteShare overview today.
                </p>
            </div>

            {/* Stats */}
            <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-4">
                <DashboardCard
                    title="Available Rides"
                    value={rides.length}
                    description="Rides currently available"
                    onClick={() => navigate(ROUTES.RIDES)}
                />

                <DashboardCard
                    title="My Bookings"
                    value={bookings.length}
                    description="Bookings you've made"
                    onClick={() => navigate(ROUTES.BOOKINGS)}
                />

                <DashboardCard
                    title="Unread Notifications"
                    value={unreadNotifications}
                    description="Pending updates"
                    onClick={() => navigate(ROUTES.NOTIFICATIONS)}
                />

                <DashboardCard
                    title="Average Rating"
                    value={averageRating}
                    description="Community feedback"
                    onClick={() => navigate(ROUTES.RATINGS)}
                />
            </div>

            {/* Middle Cards */}
            <div className="mt-8 grid gap-6 lg:grid-cols-2">

                {/* Weekly Stats */}
                <div className="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm">
                    <h2 className="mb-6 text-xl font-bold">
                        Weekly Statistics
                    </h2>

                    <div className="space-y-4">

                        <div className="flex justify-between">
                            <div className="flex items-center gap-3">
                                <Car className="text-green-600" size={20} />
                                <span>Completed Rides</span>
                            </div>

                            <span className="font-semibold">
                                {bookings.length}
                            </span>
                        </div>

                        <div className="flex justify-between">
                            <div className="flex items-center gap-3">
                                <MapPin className="text-blue-600" size={20} />
                                <span>Estimated Distance Travelled</span>
                            </div>

                            <span className="font-semibold">
                                {bookings.length * 18} km
                            </span>
                        </div>

                        <div className="flex justify-between">
                            <div className="flex items-center gap-3">
                                <Wallet className="text-yellow-600" size={20} />
                                <span>Estimated Money Saved</span>
                            </div>

                            <span className="font-semibold">
                                ₹{bookings.length * 120}
                            </span>
                        </div>

                        <div className="flex justify-between">
                            <div className="flex items-center gap-3">
                                <Leaf className="text-green-600" size={20} />
                                <span>Estimated CO₂ Saved</span>
                            </div>

                            <span className="font-semibold">
                                {(bookings.length * 2.5).toFixed(1)} kg
                            </span>
                        </div>

                    </div>
                </div>

                {/* Profile Completion */}
                <div className="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm">
                    <h2 className="mb-5 text-xl font-bold">
                        Profile Completion
                    </h2>

                    <div className="mb-3 flex justify-between">
                        <span>{profileCompletion}% Completed</span>
                        <span className="font-semibold">
                            {profileCompletion}%
                        </span>
                    </div>

                    <div className="mb-6 h-3 overflow-hidden rounded-full bg-gray-200">
                        <div
                            className="h-full rounded-full bg-green-600 transition-all duration-500"
                            style={{
                                width: `${profileCompletion}%`,
                            }}
                        />
                    </div>

                    <div className="space-y-3 text-sm">

                        <div>
                            {user?.full_name ? "✅" : "⭕"} Full Name
                        </div>

                        <div>
                            {user?.email ? "✅" : "⭕"} Email Address
                        </div>

                        <div>
                            {user?.phone_number ? "✅" : "⭕"} Phone Number
                        </div>

                        <div>
                            {user?.profile_image ? "✅" : "⭕"} Profile Picture
                        </div>

                    </div>
                </div>

            </div>

            {/* Bottom Section */}
            <div className="mt-8 grid gap-6 lg:grid-cols-2">
                            {/* Recent Activity */}
                <div className="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm">
                    <h2 className="mb-6 text-xl font-bold">
                        Recent Activity
                    </h2>

                    {recentActivities.length > 0 ? (
                        <div className="space-y-4">
                            {recentActivities
                                .slice(0, 5)
                                .map((activity, index) => (
                                    <div
                                        key={index}
                                        className="flex items-start gap-4 rounded-xl border border-gray-100 p-4 transition-all duration-200 hover:bg-gray-50 hover:shadow-sm"
                                    >
                                        <div className="mt-1 rounded-full bg-gray-100 p-2">
                                            {activity.icon}
                                        </div>

                                        <div className="flex-1">
                                            <p className="font-medium text-gray-900">
                                                {activity.title}
                                            </p>

                                            <p className="mt-1 text-sm text-gray-500">
                                                {new Date(
                                                    activity.time
                                                ).toLocaleString()}
                                            </p>
                                        </div>
                                    </div>
                                ))}
                        </div>
                    ) : (
                        <div className="flex h-52 items-center justify-center rounded-xl border border-dashed border-gray-300">
                            <p className="text-gray-500">
                                No recent activity yet.
                            </p>
                        </div>
                    )}
                </div>

                {/* Upcoming Ride */}
                <div className="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm">
                    <div className="mb-5 flex items-center gap-3">
                        <Calendar className="text-green-600" />
                        <h2 className="text-xl font-bold">
                            Upcoming Ride
                        </h2>
                    </div>

                    {bookings.length > 0 ? (
                        <div className="flex flex-col">
                            <div>
                                <p className="text-lg font-semibold text-gray-900">
                                    You have{" "}
                                    <span className="text-green-600">
                                        {bookings.length}
                                    </span>{" "}
                                    upcoming booking
                                    {bookings.length > 1 ? "s" : ""}.
                                </p>

                                <p className="mt-2 text-gray-500">
                                    Stay updated with your ride schedule and
                                    never miss a commute.
                                </p>
                            </div>

                            <button
                                onClick={() =>
                                    navigate(ROUTES.BOOKINGS)
                                }
                                className="mt-8 w-fit rounded-xl bg-green-600 px-5 py-2.5 text-white transition-all hover:bg-green-700 hover:shadow-md"
                            >
                                View My Bookings
                            </button>
                        </div>
                    ) : (
                        <div className="flex flex-col">

                            <div>
                                <p className="text-lg font-semibold">
                                    No upcoming rides
                                </p>

                                <p className="mt-2 text-gray-500">
                                    Browse available rides and reserve your next
                                    commute in just a few clicks.
                                </p>
                            </div>

                            <button
                                onClick={() =>
                                    navigate(ROUTES.RIDES)
                                }
                                className="mt-8 w-fit rounded-xl bg-green-600 px-5 py-2.5 text-white transition-all hover:bg-green-700 hover:shadow-md"
                            >
                                Browse Available Rides
                            </button>
                        </div>
                    )}
                </div>
            </div>
        </Layout>
    );
}
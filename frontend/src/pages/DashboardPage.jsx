import { useEffect } from "react";

import DashboardCard from "../components/common/DashboardCard";
import Layout from "../components/ui/Layout";

import useAuth from "../hooks/useAuth";
import useBookings from "../hooks/useBookings";
import useNotifications from "../hooks/useNotifications";
import useRatings from "../hooks/useRatings";
import useRides from "../hooks/useRides";

export default function DashboardPage() {
    const { user } = useAuth();

    const { rides } = useRides();

    const { bookings } = useBookings();

    const { notifications } = useNotifications();

    const {
        ratings,
        loadRatings,
    } = useRatings();

    useEffect(() => {
        if (user?.id) {
            loadRatings(user.id);
        }
    }, [user?.id]);

    const unreadNotifications =
        notifications.filter(
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

    return (
        <Layout>
            <div className="mb-8">
                <h1 className="text-3xl font-bold text-gray-800">
                    Welcome,
                    <span className="text-green-600">
                        {" "}
                        {user?.full_name}
                    </span>
                </h1>

                <p className="mt-2 text-gray-500">
                    Here's an overview of your activity.
                </p>
            </div>

            <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-4">
                <DashboardCard
                    title="Available Rides"
                    value={rides.length}
                    description="Current rides"
                />

                <DashboardCard
                    title="My Bookings"
                    value={bookings.length}
                    description="Active bookings"
                />

                <DashboardCard
                    title="Notifications"
                    value={unreadNotifications}
                    description="Unread notifications"
                />

                <DashboardCard
                    title="Average Rating"
                    value={averageRating}
                    description="Your rating"
                />
            </div>
        </Layout>
    );
}
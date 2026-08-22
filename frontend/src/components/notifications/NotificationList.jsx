import { Bell } from "lucide-react";
import NotificationCard from "./NotificationCard";

export default function NotificationList({
    notifications,
    onMarkRead,
}) {
    if (notifications.length === 0) {
        return (
            <div className="rounded-2xl border border-dashed border-gray-300 bg-gray-50 py-16 text-center">
                <Bell
                    size={42}
                    className="mx-auto mb-4 text-gray-400"
                />

                <h3 className="text-xl font-semibold text-gray-700">
                    No Notifications
                </h3>

                <p className="mt-2 text-gray-500">
                    You're all caught up. New booking updates,
                    ratings, ride changes and SOS alerts will
                    appear here.
                </p>
            </div>
        );
    }

    const unreadCount = notifications.filter(
        (notification) => !notification.is_read
    ).length;

    const sortedNotifications = [...notifications].sort(
        (a, b) => Number(a.is_read) - Number(b.is_read)
    );

    return (
        <div className="space-y-6">

            <div className="flex flex-wrap items-center justify-between gap-3 rounded-2xl border border-gray-200 bg-white p-5 shadow-sm">

                <div>
                    <h2 className="text-lg font-semibold text-gray-900">
                        Notification Center
                    </h2>

                    <p className="text-sm text-gray-500">
                        Stay updated with all your ride activity.
                    </p>
                </div>

                <div className="flex gap-3">

                    <span className="rounded-full bg-blue-100 px-4 py-2 text-sm font-medium text-blue-700">
                        Total: {notifications.length}
                    </span>

                    <span className="rounded-full bg-yellow-100 px-4 py-2 text-sm font-medium text-yellow-700">
                        Unread: {unreadCount}
                    </span>

                </div>

            </div>

            <div className="space-y-4">
                {sortedNotifications.map((notification) => (
                    <NotificationCard
                        key={notification.id}
                        notification={notification}
                        onMarkRead={onMarkRead}
                    />
                ))}
            </div>

        </div>
    );
}
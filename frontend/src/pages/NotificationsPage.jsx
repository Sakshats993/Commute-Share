import toast from "react-hot-toast";
import { Bell, CheckCheck } from "lucide-react";

import Layout from "../components/ui/Layout";
import LoadingSpinner from "../components/ui/LoadingSpinner";
import EmptyState from "../components/ui/EmptyState";

import NotificationList from "../components/notifications/NotificationList";

import useNotifications from "../hooks/useNotifications";

export default function NotificationsPage() {
    const {
        notifications,
        loading,
        markRead,
        markAllRead,
    } = useNotifications();

    async function handleMarkRead(id) {
        try {
            await markRead(id);

            toast.success(
                "Notification marked as read."
            );
        } catch (error) {
            toast.error(
                error.response?.data?.detail ??
                    "Failed to update notification."
            );
        }
    }

    async function handleMarkAllRead() {
        try {
            await markAllRead();

            toast.success(
                "All notifications marked as read."
            );
        } catch (error) {
            toast.error(
                error.response?.data?.detail ??
                    "Failed to update notifications."
            );
        }
    }

    if (loading) {
        return (
            <Layout>
                <div className="flex justify-center py-24">
                    <LoadingSpinner />
                </div>
            </Layout>
        );
    }

    const unreadCount = notifications.filter(
        (notification) => !notification.is_read
    ).length;

    return (
        <Layout>
            <div className="space-y-8">
                <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
                    <div>
                        <div className="flex items-center gap-3">
                            <Bell
                                size={32}
                                className="text-blue-600"
                            />

                            <h1 className="text-4xl font-bold text-gray-900">
                                Notifications
                            </h1>
                        </div>

                        <p className="mt-2 text-gray-500">
                            Stay updated with your ride activity and account alerts.
                        </p>
                    </div>

                    {notifications.length > 0 && (
                        <button
                            onClick={handleMarkAllRead}
                            className="flex items-center justify-center gap-2 rounded-xl bg-blue-600 px-6 py-3 font-medium text-white transition hover:bg-blue-700"
                        >
                            <CheckCheck size={18} />
                            Mark All Read
                        </button>
                    )}
                </div>

                {notifications.length > 0 && (
                    <div className="rounded-2xl border border-gray-200 bg-white p-5 shadow-sm">
                        <div className="flex flex-wrap gap-3">
                            <span className="rounded-full bg-blue-100 px-4 py-2 text-sm font-medium text-blue-700">
                                Total: {notifications.length}
                            </span>

                            <span className="rounded-full bg-yellow-100 px-4 py-2 text-sm font-medium text-yellow-700">
                                Unread: {unreadCount}
                            </span>
                        </div>
                    </div>
                )}

                {notifications.length === 0 ? (
                    <EmptyState
                        title="No Notifications"
                        description="You don't have any notifications yet."
                    />
                ) : (
                    <div className="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm">
                        <NotificationList
                            notifications={notifications}
                            onMarkRead={handleMarkRead}
                        />
                    </div>
                )}
            </div>
        </Layout>
    );
}
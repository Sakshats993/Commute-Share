import toast from "react-hot-toast";

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
                <LoadingSpinner />
            </Layout>
        );
    }

    return (
        <Layout>
            <div className="space-y-6">

                <div className="flex justify-between items-center">

                    <h1 className="text-3xl font-bold">
                        Notifications
                    </h1>

                    {notifications.length > 0 && (
                        <button
                            onClick={handleMarkAllRead}
                            className="bg-blue-600 hover:bg-blue-700 text-white px-5 py-2 rounded-lg"
                        >
                            Mark All Read
                        </button>
                    )}

                </div>

                {notifications.length === 0 ? (
                    <EmptyState
                        title="No Notifications"
                        description="You don't have any notifications yet."
                    />
                ) : (
                    <NotificationList
                        notifications={notifications}
                        onMarkRead={handleMarkRead}
                    />
                )}

            </div>
        </Layout>
    );
}
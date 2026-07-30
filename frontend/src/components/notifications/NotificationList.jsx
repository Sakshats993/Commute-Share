import NotificationCard from "./NotificationCard";

export default function NotificationList({
    notifications,
    onMarkRead,
}) {
    if (notifications.length === 0) {
        return (
            <div className="text-center py-16 text-gray-500">
                No notifications found.
            </div>
        );
    }

    return (
        <div className="space-y-4">
            {notifications.map((notification) => (
                <NotificationCard
                    key={notification.id}
                    notification={notification}
                    onMarkRead={onMarkRead}
                />
            ))}
        </div>
    );
}
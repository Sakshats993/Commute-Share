import {
    Bell,
    CheckCircle2,
    Star,
    Car,
    ShieldAlert,
    Clock,
} from "lucide-react";

export default function NotificationCard({
    notification,
    onMarkRead,
}) {
    const getNotificationMeta = (type = "") => {
        switch (type.toLowerCase()) {
            case "booking":
            case "booking_confirmed":
                return {
                    icon: CheckCircle2,
                    iconColor: "text-green-600",
                    badge: "Booking",
                    badgeColor:
                        "bg-green-100 text-green-700",
                };

            case "ride":
            case "ride_updated":
                return {
                    icon: Car,
                    iconColor: "text-blue-600",
                    badge: "Ride",
                    badgeColor:
                        "bg-blue-100 text-blue-700",
                };

            case "rating":
                return {
                    icon: Star,
                    iconColor: "text-yellow-500",
                    badge: "Rating",
                    badgeColor:
                        "bg-yellow-100 text-yellow-700",
                };

            case "sos":
                return {
                    icon: ShieldAlert,
                    iconColor: "text-red-600",
                    badge: "SOS",
                    badgeColor:
                        "bg-red-100 text-red-700",
                };

            default:
                return {
                    icon: Bell,
                    iconColor: "text-blue-600",
                    badge: notification.type || "General",
                    badgeColor:
                        "bg-gray-100 text-gray-700",
                };
        }
    };

    const meta = getNotificationMeta(
        notification.type
    );

    const Icon = meta.icon;

    return (
        <div
            className={`rounded-2xl border p-5 shadow-sm transition duration-200 hover:shadow-md ${
                notification.is_read
                    ? "bg-white border-gray-200"
                    : "border-blue-300 bg-blue-50"
            }`}
        >
            <div className="flex items-start justify-between gap-4">

                <div className="flex flex-1 gap-4">

                    <div
                        className={`mt-1 rounded-full bg-white p-3 shadow ${meta.iconColor}`}
                    >
                        <Icon size={22} />
                    </div>

                    <div className="flex-1">

                        <div className="flex flex-wrap items-center gap-2">

                            <h3 className="text-lg font-semibold text-gray-900">
                                {notification.title}
                            </h3>

                            <span
                                className={`rounded-full px-3 py-1 text-xs font-medium ${meta.badgeColor}`}
                            >
                                {meta.badge}
                            </span>

                            {!notification.is_read && (
                                <span className="rounded-full bg-blue-600 px-2 py-1 text-xs font-medium text-white">
                                    New
                                </span>
                            )}

                        </div>

                        <p className="mt-2 text-gray-600 leading-relaxed">
                            {notification.message}
                        </p>

                        <div className="mt-4 flex flex-wrap items-center gap-4 text-sm text-gray-500">

                            <div className="flex items-center gap-2">
                                <Clock size={15} />
                                {new Date(
                                    notification.created_at
                                ).toLocaleString()}
                            </div>

                        </div>

                    </div>

                </div>

                {!notification.is_read && (
                    <button
                        onClick={() =>
                            onMarkRead(notification.id)
                        }
                        className="rounded-xl bg-blue-600 px-4 py-2 text-sm font-medium text-white transition hover:bg-blue-700"
                    >
                        Mark Read
                    </button>
                )}

            </div>
        </div>
    );
}
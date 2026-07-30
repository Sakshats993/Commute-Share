import { Bell } from "lucide-react";

export default function NotificationCard({
    notification,
    onMarkRead,
}) {
    return (
        <div
            className={`rounded-xl shadow p-5 border ${
                notification.is_read
                    ? "bg-white"
                    : "bg-blue-50 border-blue-300"
            }`}
        >
            <div className="flex justify-between items-start">

                <div className="flex gap-3">

                    <Bell
                        className="text-blue-600 mt-1"
                        size={20}
                    />

                    <div>

                        <h3 className="font-semibold text-lg">
                            {notification.title}
                        </h3>

                        <p className="text-gray-600 mt-1">
                            {notification.message}
                        </p>

                        <div className="flex gap-4 mt-3 text-sm text-gray-500">

                            <span>
                                {notification.type}
                            </span>

                            <span>
                                {new Date(
                                    notification.created_at
                                ).toLocaleString()}
                            </span>

                        </div>

                    </div>

                </div>

                {!notification.is_read && (
                    <button
                        onClick={() =>
                            onMarkRead(notification.id)
                        }
                        className="bg-blue-600 hover:bg-blue-700 text-white px-3 py-2 rounded-lg text-sm"
                    >
                        Mark Read
                    </button>
                )}

            </div>
        </div>
    );
}
import { useEffect, useState } from "react";

import * as notificationApi from "../api/notifications";

export default function useNotifications() {
    const [notifications, setNotifications] =
        useState([]);

    const [loading, setLoading] =
        useState(true);

    async function loadNotifications() {
        try {
            setLoading(true);

            const data =
                await notificationApi.getNotifications();

            setNotifications(data);
        } finally {
            setLoading(false);
        }
    }

    async function loadUnread() {
        return notificationApi.getUnreadNotifications();
    }

    async function markRead(id) {
        const updated =
            await notificationApi.markNotificationRead(
                id
            );

        setNotifications((prev) =>
            prev.map((notification) =>
                notification.id === id
                    ? updated
                    : notification
            )
        );
    }

    async function markAllRead() {
        await notificationApi.markAllNotificationsRead();

        setNotifications((prev) =>
            prev.map((notification) => ({
                ...notification,
                is_read: true,
            }))
        );
    }

    useEffect(() => {
        loadNotifications();
    }, []);

    return {
        notifications,
        loading,
        loadNotifications,
        loadUnread,
        markRead,
        markAllRead,
    };
}
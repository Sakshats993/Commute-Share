import { useState } from "react";

import * as adminApi from "../api/admin";

export default function useAdmin() {
    const [statistics, setStatistics] =
        useState(null);

    const [users, setUsers] =
        useState([]);

    const [rides, setRides] =
        useState([]);

    const [bookings, setBookings] =
        useState([]);

    const [sosEvents, setSosEvents] = useState([]);

    const [loading, setLoading] =
        useState(false);

    async function loadDashboard() {
        try {
            setLoading(true);

            const [
                stats,
                userData,
                rideData,
                bookingData,
                safetyEvents,
            ] = await Promise.all([
                adminApi.getDashboardStatistics(),
                adminApi.getUsers(),
                adminApi.getRides(),
                adminApi.getBookings(),
                adminApi.getSosEvents(),
            ]);

            setStatistics(stats);
            setUsers(userData);
            setRides(rideData);
            setBookings(bookingData);
            setSosEvents(safetyEvents);
        } finally {
            setLoading(false);
        }
    }

    async function activate(id) {
        const updated =
            await adminApi.activateUser(id);

        setUsers((prev) =>
            prev.map((user) =>
                user.id === id
                    ? updated
                    : user
            )
        );
    }

    async function deactivate(id) {
        const updated =
            await adminApi.deactivateUser(id);

        setUsers((prev) =>
            prev.map((user) =>
                user.id === id
                    ? updated
                    : user
            )
        );
    }

    async function updateSos(id, action) {
        const updated = await adminApi.updateSosEvent(id, action);
        setSosEvents((items) => items.map((event) => event.id === id ? updated : event));
        return updated;
    }

    return {
        statistics,
        users,
        rides,
        bookings,
        sosEvents,
        loading,
        loadDashboard,
        activate,
        deactivate,
        updateSos,
    };
}

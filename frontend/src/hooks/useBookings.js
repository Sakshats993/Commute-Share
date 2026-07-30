import { useEffect, useState } from "react";

import * as bookingsApi from "../api/bookings";

export default function useBookings() {
    const [bookings, setBookings] = useState([]);
    const [statistics, setStatistics] = useState(null);
    const [loading, setLoading] = useState(false);

    async function loadBookings() {
        try {
            setLoading(true);

            const data = await bookingsApi.getMyBookings();

            setBookings(data);
        } finally {
            setLoading(false);
        }
    }

    async function loadStatistics() {
        try {
            const data =
                await bookingsApi.getBookingStatistics();

            setStatistics(data);
        } catch {
            setStatistics(null);
        }
    }

    async function cancel(bookingId) {
        await bookingsApi.cancelBooking(bookingId);

        setBookings((prev) =>
            prev.filter(
                (booking) => booking.id !== bookingId
            )
        );
    }

    useEffect(() => {
        loadBookings();
        loadStatistics();
    }, []);

    return {
        bookings,
        statistics,
        loading,
        cancel,
        loadBookings,
        loadStatistics,
    };
}
import { useState } from "react";
import toast from "react-hot-toast";

import Layout from "../components/ui/Layout";
import LoadingSpinner from "../components/ui/LoadingSpinner";
import EmptyState from "../components/ui/EmptyState";

import BookingStatistics from "../components/bookings/BookingStatistics";
import BookingList from "../components/bookings/BookingList";
import CancelBookingModal from "../components/bookings/CancelBookingModal";

import useBookings from "../hooks/useBookings";

export default function BookingsPage() {
    const {
        bookings,
        statistics,
        loading,
        cancel,
        loadBookings,
        loadStatistics,
    } = useBookings();

    const [selectedBooking, setSelectedBooking] =
        useState(null);

    async function handleCancel(bookingId) {
        try {
            await cancel(bookingId);

            toast.success("Booking cancelled.");

            setSelectedBooking(null);

            await loadBookings();
            await loadStatistics();
        } catch (error) {
            toast.error(
                error.response?.data?.detail ??
                    "Failed to cancel booking."
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
            <div className="space-y-8">

                <h1 className="text-3xl font-bold">
                    My Bookings
                </h1>

                <BookingStatistics
                    statistics={statistics}
                />

                {bookings.length === 0 ? (
                    <EmptyState
                        title="No Bookings"
                        description="You haven't booked any rides yet."
                    />
                ) : (
                    <BookingList
                        bookings={bookings}
                        onCancel={setSelectedBooking}
                    />
                )}

                <CancelBookingModal
                    booking={selectedBooking}
                    onConfirm={handleCancel}
                    onCancel={() =>
                        setSelectedBooking(null)
                    }
                />

            </div>
        </Layout>
    );
}
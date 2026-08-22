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
        refreshBookings,
    } = useBookings();

    const [selectedBooking, setSelectedBooking] =
        useState(null);

    async function handleCancel(bookingId) {
        try {
            await cancel(bookingId);

            toast.success("Booking cancelled successfully.");

            setSelectedBooking(null);

            await Promise.all([
                loadBookings(),
                loadStatistics(),
            ]);
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
                <div className="flex justify-center py-24">
                    <LoadingSpinner />
                </div>
            </Layout>
        );
    }

    return (
        <Layout>
            <div className="space-y-8">
                {/* Header */}
                <div className="flex flex-col gap-2">
                    <h1 className="text-4xl font-bold text-gray-900">
                        My Bookings
                    </h1>

                    <p className="text-gray-500">
                        View, manage and cancel your ride bookings.
                    </p>
                </div>

                {/* Statistics */}
                <div className="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm">
                    <BookingStatistics
                        statistics={statistics}
                    />
                </div>

                {/* Booking List */}
                <div className="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm">
                    {bookings.length === 0 ? (
                        <EmptyState
                            title="No Bookings Yet"
                            description="You haven't booked any rides yet. Browse available rides to get started."
                        />
                    ) : (
                        <>
                            <div className="mb-6 flex items-center justify-between">
                                <h2 className="text-xl font-semibold text-gray-900">
                                    Booking History
                                </h2>

                                <span className="rounded-full bg-blue-100 px-3 py-1 text-sm font-medium text-blue-700">
                                    {bookings.length}{" "}
                                    {bookings.length === 1
                                        ? "Booking"
                                        : "Bookings"}
                                </span>
                            </div>

                        <BookingList
                            bookings={bookings}
                            onCancel={setSelectedBooking}
                            onRideUpdated={refreshBookings}
                        />
                        </>
                    )}
                </div>

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
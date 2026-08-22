   import {
        useContext,
        useEffect,
        useState,
    } from "react";
    import { useParams } from "react-router-dom";
    import toast from "react-hot-toast";
    import {
        MapPin,
        Users,
        IndianRupee,
        Car,
        FileText,
        CalendarDays,
    } from "lucide-react";

    import Layout from "../components/ui/Layout";
    import LoadingSpinner from "../components/ui/LoadingSpinner";

    import {
        getRide,
        startRide,
        endRide,
        confirmRide,
    } from "../api/rides";

    import {
        bookRide,
        getRideBookings,
        confirmBooking,
    } from "../api/bookings";

    import AuthContext from "../context/AuthContext";

    export default function RideDetailsPage() {
        const { rideId } = useParams();
        const { user } = useContext(AuthContext);

        const [bookings, setBookings] = useState([]);
        const [bookingsLoading, setBookingsLoading] =
            useState(false);

        const [confirmingBooking, setConfirmingBooking] =
            useState(null);

        const [ride, setRide] = useState(null);
        const [loading, setLoading] = useState(true);
        const [bookingLoading, setBookingLoading] = useState(false);
        const [rideActionLoading, setRideActionLoading] =
            useState(false);

        useEffect(() => {
            loadRide();
        }, [rideId]);

        useEffect(() => {
            loadBookings();
        }, [ride, user]);

        async function loadBookings() {
            if (!user || !ride) {
                return;
            }

            if (Number(user.id) !== Number(ride.driver_id)) {
                return;
            }

            try {
                setBookingsLoading(true);

                const data =
                    await getRideBookings(ride.id);

                setBookings(data);
            } catch (error) {
                toast.error(
                    error.response?.data?.detail ??
                        "Failed to load booking requests."
                );
            } finally {
                setBookingsLoading(false);
            }
        }

        async function loadRide() {
            try {
                setLoading(true);

                const data = await getRide(rideId);

                setRide(data);
            } catch (error) {
                toast.error(
                    error.response?.data?.detail ??
                        "Failed to load ride."
                );
            } finally {
                setLoading(false);
            }
        }

        async function handleBookRide() {
            try {
                setBookingLoading(true);

                await bookRide(ride.id);

                toast.success("Ride booked successfully!");

                await loadRide();
            } catch (error) {
                toast.error(
                    error.response?.data?.detail ??
                        "Booking failed."
                );
            } finally {
                setBookingLoading(false);
            }
        }
        async function handleConfirmBooking(
            bookingId
        ) {
            try {
                setConfirmingBooking(bookingId);

                await confirmBooking(bookingId);

                toast.success(
                    "Booking confirmed successfully."
                );

                await Promise.all([
                    loadRide(),
                    loadBookings(),
                ]);
            } catch (error) {
                toast.error(
                    error.response?.data?.detail ??
                        "Failed to confirm booking."
                );
            } finally {
                setConfirmingBooking(null);
            }
        }
        async function handleStartRide() {
            try {
                setRideActionLoading(true);

                const updatedRide =
                    await startRide(ride.id);

                setRide(updatedRide);

                toast.success(
                    "Ride started successfully."
                );

                await loadBookings();
            } catch (error) {
                toast.error(
                    error.response?.data?.detail ??
                        "Failed to start ride."
                );
            } finally {
                setRideActionLoading(false);
            }
        }
        async function handleConfirmDropoff() {
            try {
                setRideActionLoading(true);

                const updatedRide =
                    await confirmRide(ride.id);

                setRide(updatedRide);

                toast.success(
                    "Ride completed successfully."
                );

                await loadBookings();
            } catch (error) {
                toast.error(
                    error.response?.data?.detail ??
                        "Failed to confirm drop-off."
                );
            } finally {
                setRideActionLoading(false);
            }
        }
        async function handleEndRide() {
            try {
                setRideActionLoading(true);

                const updatedRide =
                    await endRide(ride.id);

                setRide(updatedRide);

                toast.success(
                    "Ride ended. Waiting for passenger confirmation."
                );

                await loadBookings();
            } catch (error) {
                toast.error(
                    error.response?.data?.detail ??
                        "Failed to end ride."
                );
            } finally {
                setRideActionLoading(false);
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

        if (!ride) {
            return (
                <Layout>
                    <div className="rounded-2xl border bg-white p-12 text-center shadow-sm">
                        <h2 className="text-2xl font-bold text-gray-900">
                            Ride not found
                        </h2>

                        <p className="mt-2 text-gray-500">
                            The requested ride does not exist.
                        </p>
                    </div>
                </Layout>
            );
        }

        return (
    <Layout>
        <div className="mx-auto max-w-7xl">

            {/* ========================================= */}
            {/* Hero Banner */}
            {/* ========================================= */}

            <div className="overflow-hidden rounded-3xl bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 p-10 text-white shadow-xl">

                <div className="flex flex-col items-center text-center">

                    <h1 className="text-4xl font-bold lg:text-5xl">
                        {ride.pickup_location}
                        <span className="mx-4 text-blue-200">→</span>
                        {ride.destination_location}
                    </h1>

                    <div className="mt-5 flex flex-wrap items-center justify-center gap-4">

                        <span className="rounded-full bg-green-500/20 px-4 py-2 text-sm font-semibold text-green-100">
                            🟢 {ride.status}
                        </span>

                        <span className="rounded-full bg-white/15 px-4 py-2 text-sm">
                            🕒{" "}
                            {new Date(
                                ride.departure_time
                            ).toLocaleString()}
                        </span>

                    </div>

                    <div className="mt-8">

                        <p className="text-sm uppercase tracking-widest text-blue-200">
                            Price Per Seat
                        </p>

                        <h2 className="mt-1 text-5xl font-bold">
                            ₹{ride.price_per_seat}
                        </h2>

                    </div>

                </div>

            </div>               
            <div className="mt-8 grid gap-6 lg:grid-cols-3">

                {/* Driver */}

                <div className="flex h-full flex-col rounded-2xl border bg-white p-6 text-center shadow-sm transition hover:shadow-lg">

                    <h2 className="mb-5 text-lg font-semibold">
                        👤 Driver
                    </h2>

                    <div className="mx-auto flex h-20 w-20 items-center justify-center rounded-full bg-blue-600 text-3xl font-bold text-white">

                        {ride.driver.full_name.charAt(0)}

                    </div>

                    <h3 className="mt-5 text-xl font-bold text-gray-900">
                        {ride.driver.full_name}
                    </h3>

                    <p className="mt-1 text-gray-500">
                        Driver
                    </p>

                    <p className="mt-3 text-sm text-gray-500">
                        {ride.driver.email}
                    </p>

                    <div className="mt-6 w-full space-y-3">

                    <div className="flex items-center justify-between rounded-xl bg-yellow-50 px-4 py-3">
                        <span className="font-medium text-gray-700">
                            ⭐ Rating
                        </span>

                        <span className="font-bold text-yellow-700">
                            {ride.driver.average_rating.toFixed(1)}
                        </span>
                    </div>

                    <div className="flex items-center justify-between rounded-xl bg-blue-50 px-4 py-3">
                        <span className="font-medium text-gray-700">
                            💬 Reviews
                        </span>

                        <span className="font-bold text-blue-700">
                            {ride.driver.review_count}
                        </span>
                    </div>

                    <div className="flex items-center justify-between rounded-xl bg-green-50 px-4 py-3">
                        <span className="font-medium text-gray-700">
                            🚗 Completed
                        </span>

                        <span className="font-bold text-green-700">
                            {ride.driver.completed_rides}
                        </span>
                    </div>

                    <div className="flex items-center justify-between rounded-xl bg-gray-50 px-4 py-3">
                        <span className="font-medium text-gray-700">
                            Verification
                        </span>

                        <span
                            className={`font-bold ${
                                ride.driver.is_verified
                                    ? "text-green-600"
                                    : "text-red-500"
                            }`}
                        >
                            {ride.driver.is_verified
                                ? "✔ Verified"
                                : "❌ Not Verified"}
                        </span>
                    </div>

                </div>
                </div>                       
                {/* Vehicle */}

                <div className="flex h-full flex-col rounded-2xl border bg-white p-6 shadow-sm transition hover:shadow-lg">

                    <h2 className="mb-5 text-lg font-semibold">
                        🚘 Vehicle
                    </h2>

                    <div className="space-y-5">

                        <div>

                            <p className="text-sm text-gray-500">
                                Vehicle
                            </p>

                            <h3 className="text-xl font-bold">
                                {ride.vehicle.make}{" "}
                                {ride.vehicle.model}
                            </h3>

                        </div>

                        <div>

                            <p className="text-sm text-gray-500">
                                Color
                            </p>

                            <p className="font-medium">
                                {ride.vehicle.color}
                            </p>

                        </div>

                        <div>

                            <p className="text-sm text-gray-500">
                                Registration
                            </p>

                            <p className="font-medium">
                                {ride.vehicle.registration_number}
                            </p>

                        </div>

                        <div>

                            <p className="text-sm text-gray-500">
                                Capacity
                            </p>

                            <p className="font-medium">
                                {ride.vehicle.seating_capacity} Seats
                            </p>

                        </div>

                    </div>

                </div>

                {/* Summary */}

                <div className="flex h-full flex-col rounded-2xl border bg-white p-6 shadow-sm transition hover:shadow-lg">

                    <h2 className="mb-5 text-lg font-semibold">
                        💼 Trip Summary
                    </h2>

                    <div className="space-y-5">

                        <div>

                            <p className="text-sm text-gray-500">
                                Seats
                            </p>

                            <p className="text-xl font-bold">
                                {ride.available_seats} /{" "}
                                {ride.total_seats}
                            </p>

                        </div>

                        <div>

                            <p className="text-sm text-gray-500">
                                Fare
                            </p>

                            <p className="text-xl font-bold text-green-600">
                                ₹{ride.price_per_seat}
                            </p>

                        </div>

                        <div>

                            <p className="text-sm text-gray-500">
                                Status
                            </p>

                            <span className="rounded-full bg-green-100 px-3 py-1 text-sm font-semibold text-green-700">
                                {ride.status}
                            </span>

                        </div>

                    </div>

                </div>

            </div>
                        {/* ========================================= */}
            {/* Route */}
            {/* ========================================= */}

            <div className="mt-8 rounded-2xl border bg-white p-8 shadow-sm">

                <h2 className="mb-8 text-2xl font-bold">
                    📍 Route
                </h2>

                <div className="flex flex-col">

                    {/* Pickup */}

                    <div className="flex items-start gap-5">

                        <div className="mt-1 flex h-12 w-12 items-center justify-center rounded-full bg-green-100">
                            <MapPin
                                size={22}
                                className="text-green-600"
                            />
                        </div>

                        <div>

                            <p className="text-sm uppercase tracking-wide text-gray-500">
                                Pickup
                            </p>

                            <h3 className="mt-1 text-xl font-semibold">
                                {ride.pickup_location}
                            </h3>

                        </div>

                    </div>

                    {/* Route Line */}

                    <div className="ml-6 flex h-16 items-center">

                        <div className="h-full border-l-2 border-dashed border-gray-300"></div>

                    </div>

                    {/* Destination */}

                    <div className="flex items-start gap-5">

                        <div className="mt-1 flex h-12 w-12 items-center justify-center rounded-full bg-red-100">
                            <MapPin
                                size={22}
                                className="text-red-600"
                            />
                        </div>

                        <div>

                            <p className="text-sm uppercase tracking-wide text-gray-500">
                                Destination
                            </p>

                            <h3 className="mt-1 text-xl font-semibold">
                                {ride.destination_location}
                            </h3>

                        </div>

                    </div>

                </div>

            </div>

            {/* ========================================= */}
            {/* Driver Notes */}
            {/* ========================================= */}

            {ride.notes && (

                <div className="mt-8 rounded-2xl border bg-white p-8 shadow-sm">

                    <h2 className="mb-5 text-2xl font-bold">
                        📝 Driver Notes
                    </h2>

                    <div className="rounded-xl bg-gray-50 p-6">

                        <p className="text-lg leading-8 text-gray-700">
                            {ride.notes}
                        </p>

                    </div>

                </div>

            )}

            {/* ========================================= */}
            {/* Driver Booking Requests */}
            {/* ========================================= */}

            {user &&
                Number(ride.driver_id) === Number(user.id) && (
                    <div className="mt-8 rounded-3xl border bg-white p-8 shadow-sm">

                        <div className="flex items-center justify-between">
                            <div>
                                <h2 className="text-2xl font-bold text-gray-900">
                                    Passenger Requests
                                </h2>

                                <p className="mt-1 text-gray-500">
                                    Manage passengers requesting to join this ride.
                                </p>
                            </div>

                            <span className="rounded-full bg-blue-100 px-4 py-2 text-sm font-semibold text-blue-700">
                                {bookings.length}{" "}
                                {bookings.length === 1
                                    ? "Passenger"
                                    : "Passengers"}
                            </span>
                        </div>

                        {bookingsLoading ? (
                            <div className="mt-8 flex justify-center">
                                <LoadingSpinner />
                            </div>
                        ) : bookings.length === 0 ? (
                            <div className="mt-8 rounded-2xl bg-gray-50 p-8 text-center">
                                <p className="text-gray-500">
                                    No passenger requests yet.
                                </p>
                            </div>
                        ) : (
                            <div className="mt-8 space-y-4">

                                {bookings.map((booking) => {

                                    const bookingStatus =
                                        String(
                                            booking.status
                                        ).toLowerCase();

                                    const isPending =
                                        bookingStatus ===
                                        "pending";

                                    const isConfirmed =
                                        bookingStatus ===
                                        "confirmed";

                                    const isCancelled =
                                        bookingStatus ===
                                        "cancelled";

                                    return (
                                        <div
                                            key={booking.id}
                                            className="flex flex-col gap-4 rounded-2xl border border-gray-200 bg-gray-50 p-5 md:flex-row md:items-center md:justify-between"
                                        >

                                            <div>
                                                <h3 className="text-lg font-semibold text-gray-900">
                                                    Passenger
                                                </h3>

                                                <p className="text-sm text-gray-500">
                                                    Passenger ID:{" "}
                                                    {booking.passenger_id}
                                                </p>

                                                <p className="mt-2 text-sm">
                                                    Booking #{booking.id}
                                                </p>
                                            </div>

                                            <div className="flex items-center gap-3">

                                                {isPending && (
                                                    <>
                                                        <span className="rounded-full bg-yellow-100 px-4 py-2 text-sm font-semibold text-yellow-700">
                                                            🟡 Pending
                                                        </span>

                                                        <button
                                                            onClick={() =>
                                                                handleConfirmBooking(
                                                                    booking.id
                                                                )
                                                            }
                                                            disabled={
                                                                confirmingBooking ===
                                                                booking.id
                                                            }
                                                            className="rounded-xl bg-green-600 px-5 py-2.5 font-semibold text-white transition hover:bg-green-700 disabled:cursor-not-allowed disabled:bg-gray-400"
                                                        >
                                                            {confirmingBooking ===
                                                            booking.id
                                                                ? "Confirming..."
                                                                : "✓ Confirm Booking"}
                                                        </button>
                                                    </>
                                                )}

                                                {isConfirmed && (
                                                    <span className="rounded-full bg-green-100 px-4 py-2 text-sm font-semibold text-green-700">
                                                        ✓ Confirmed
                                                    </span>
                                                )}

                                                {isCancelled && (
                                                    <span className="rounded-full bg-red-100 px-4 py-2 text-sm font-semibold text-red-700">
                                                        ✕ Cancelled
                                                    </span>
                                                )}

                                            </div>

                                        </div>
                                    );
                                })}

                            </div>
                        )}

                    </div>
                )}
                
            {/* ========================================= */}
            {/* Booking */}
            {/* ========================================= */}

            {user &&
                Number(user.id) !== Number(ride.driver_id) && (
                <div className="mt-8 rounded-3xl border bg-gradient-to-r from-green-50 to-emerald-50 p-8 shadow-sm">

                    <div className="text-center">

                        <p className="text-sm uppercase tracking-widest text-gray-500">
                            Price Per Seat
                        </p>

                        <h2 className="mt-2 text-5xl font-bold text-green-600">
                            ₹{ride.price_per_seat}
                        </h2>

                        <p className="mt-5 text-lg text-gray-600">
                            {ride.available_seats} of {ride.total_seats} seats available
                        </p>

                        <button
                            onClick={handleBookRide}
                            disabled={
                                bookingLoading ||
                                ride.available_seats <= 0
                            }
                            className={`mt-8 w-full rounded-2xl py-4 text-lg font-semibold text-white transition-all duration-300 lg:w-96 ${
                                bookingLoading
                                    ? "cursor-not-allowed bg-gray-400"
                                    : ride.available_seats <= 0
                                    ? "cursor-not-allowed bg-red-500"
                                    : "bg-green-600 hover:-translate-y-1 hover:bg-green-700 hover:shadow-xl"
                            }`}
                        >
                            {bookingLoading
                                ? "Booking Ride..."
                                : ride.available_seats <= 0
                                ? "Ride Full"
                                : "🚗 Book This Ride"}
                        </button>

                    </div>

                </div>
            )}

        </div>
    </Layout>
);
}
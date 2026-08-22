import {
    Calendar,
    CheckCircle,
    Clock,
    IndianRupee,
    MapPin,
    User,
    Car,
    Users,
    Phone,
    XCircle,
    Play,
    Square,
} from "lucide-react";

import toast from "react-hot-toast";

import useAuth from "../../hooks/useAuth";

import {
    startRide,
    endRide,
    confirmRide,
} from "../../api/rides";

export default function BookingCard({
    booking,
    onCancel,
    onRideUpdated,
}) {
    const { user } = useAuth();

    const ride = booking.ride || {};

    const pickup =
        ride.pickup_location ??
        "Pickup";

    const destination =
        ride.destination_location ??
        "Destination";

    const departure =
        ride.departure_time;

    const price =
        ride.price_per_seat ??
        ride.price;

    const driver =
        ride.driver?.full_name ??
        ride.driver?.name ??
        ride.driver_name;

    const phone =
        ride.driver?.phone ??
        ride.driver_phone;

    const vehicle =
        ride.vehicle?.model ??
        ride.vehicle_name;

    const seats =
        ride.available_seats ??
        ride.seats_available;

    const bookingStatus =
        String(booking.status ?? "").toLowerCase();

    const rideStatus =
        String(ride.status ?? "").toLowerCase();

    const isDriver =
        Number(user?.id) === Number(ride.driver_id);

    const isConfirmed =
        bookingStatus === "confirmed";

    const isCancelled =
        bookingStatus === "cancelled";

    const isPending =
        bookingStatus === "pending";

    const isScheduled =
        rideStatus === "scheduled";

    const isInProgress =
        rideStatus === "in_progress";

    const awaitingPassengerConfirmation =
        rideStatus ===
        "awaiting_passenger_confirmation";

    const isCompleted =
        rideStatus === "completed";

    async function handleStartRide() {
        try {
            const updatedRide =
                await startRide(ride.id);

            toast.success(
                "Ride started successfully."
            );

            if (onRideUpdated) {
                onRideUpdated(updatedRide);
            }
        } catch (error) {
            toast.error(
                error.response?.data?.detail ??
                    "Failed to start ride."
            );
        }
    }

    async function handleEndRide() {
        try {
            const updatedRide =
                await endRide(ride.id);

            toast.success(
                "Ride ended. Waiting for passenger confirmation."
            );

            if (onRideUpdated) {
                onRideUpdated(updatedRide);
            }
        } catch (error) {
            toast.error(
                error.response?.data?.detail ??
                    "Failed to end ride."
            );
        }
    }

    async function handleConfirmDropoff() {
        try {
            const updatedRide =
                await confirmRide(ride.id);

            toast.success(
                "Ride completed successfully."
            );

            if (onRideUpdated) {
                onRideUpdated(updatedRide);
            }
        } catch (error) {
            toast.error(
                error.response?.data?.detail ??
                    "Failed to confirm drop-off."
            );
        }
    }

    return (
        <div className="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm transition hover:shadow-md">

            {/* ================================================= */}
            {/* Header */}
            {/* ================================================= */}

            <div className="flex flex-col gap-4 md:flex-row md:items-start md:justify-between">

                <div>

                    <div className="flex items-center gap-2 text-2xl font-bold text-gray-900">

                        <MapPin
                            size={24}
                            className="text-blue-600"
                        />

                        <span>
                            {pickup} → {destination}
                        </span>

                    </div>

                    <div className="mt-3 flex flex-wrap gap-4 text-sm text-gray-600">

                        <div className="flex items-center gap-2">

                            <Calendar size={16} />

                            {departure
                                ? new Date(
                                      departure
                                  ).toLocaleString()
                                : new Date(
                                      booking.created_at
                                  ).toLocaleString()}

                        </div>

                        {price != null && (
                            <div className="flex items-center gap-2">

                                <IndianRupee size={16} />

                                ₹{price} / seat

                            </div>
                        )}

                    </div>

                </div>

                {/* Ride Status */}

                <span
                    className={`inline-flex items-center gap-2 rounded-full px-4 py-2 text-sm font-semibold ${
                        isCompleted
                            ? "bg-green-100 text-green-700"
                            : isInProgress
                            ? "bg-blue-100 text-blue-700"
                            : awaitingPassengerConfirmation
                            ? "bg-orange-100 text-orange-700"
                            : isCancelled
                            ? "bg-red-100 text-red-700"
                            : isConfirmed
                            ? "bg-green-100 text-green-700"
                            : "bg-yellow-100 text-yellow-700"
                    }`}
                >

                    {isCompleted ? (
                        <>
                            <CheckCircle size={16} />
                            Completed
                        </>
                    ) : isInProgress ? (
                        <>
                            <Play size={16} />
                            Ride In Progress
                        </>
                    ) : awaitingPassengerConfirmation ? (
                        <>
                            <Clock size={16} />
                            Awaiting Drop-off Confirmation
                        </>
                    ) : isCancelled ? (
                        <>
                            <XCircle size={16} />
                            Cancelled
                        </>
                    ) : isConfirmed ? (
                        <>
                            <CheckCircle size={16} />
                            Confirmed
                        </>
                    ) : (
                        <>
                            <Clock size={16} />
                            Pending
                        </>
                    )}

                </span>

            </div>

            {/* ================================================= */}
            {/* Ride Information */}
            {/* ================================================= */}

            <div className="mt-6 grid gap-4 md:grid-cols-2">

                <div className="space-y-3">

                    {driver && (
                        <div className="flex items-center gap-2">

                            <User
                                size={18}
                                className="text-blue-600"
                            />

                            <span>
                                {driver}
                            </span>

                        </div>
                    )}

                    {vehicle && (
                        <div className="flex items-center gap-2">

                            <Car
                                size={18}
                                className="text-blue-600"
                            />

                            <span>
                                {vehicle}
                            </span>

                        </div>
                    )}

                    {phone &&
                        isConfirmed &&
                        !isCancelled && (
                            <div className="flex items-center gap-2">

                                <Phone
                                    size={18}
                                    className="text-blue-600"
                                />

                                <span>
                                    {phone}
                                </span>

                            </div>
                        )}

                    {seats != null && (
                        <div className="flex items-center gap-2">

                            <Users
                                size={18}
                                className="text-blue-600"
                            />

                            <span>
                                Seats Left: {seats}
                            </span>

                        </div>
                    )}

                </div>

                {/* ================================================= */}
                {/* Timeline */}
                {/* ================================================= */}

                <div className="rounded-xl bg-gray-50 p-4">

                    <h3 className="mb-3 font-semibold text-gray-800">
                        Ride Timeline
                    </h3>

                    <div className="space-y-3 text-sm">

                        {/* Requested */}

                        <div className="flex items-center gap-2 text-green-600">

                            <CheckCircle size={16} />

                            Requested

                        </div>

                        {/* Confirmed */}

                        <div
                            className={`flex items-center gap-2 ${
                                isConfirmed ||
                                isInProgress ||
                                awaitingPassengerConfirmation ||
                                isCompleted
                                    ? "text-green-600"
                                    : "text-gray-400"
                            }`}
                        >

                            <CheckCircle size={16} />

                            Confirmed

                        </div>

                        {/* Started */}

                        <div
                            className={`flex items-center gap-2 ${
                                isInProgress ||
                                awaitingPassengerConfirmation ||
                                isCompleted
                                    ? "text-green-600"
                                    : "text-gray-400"
                            }`}
                        >

                            <Play size={16} />

                            Ride Started

                        </div>

                        {/* Completed */}

                        <div
                            className={`flex items-center gap-2 ${
                                isCompleted
                                    ? "text-green-600"
                                    : "text-gray-400"
                            }`}
                        >

                            <CheckCircle size={16} />

                            Completed

                        </div>

                    </div>

                </div>

            </div>

            {/* ================================================= */}
            {/* DRIVER CONTROLS */}
            {/* ================================================= */}

            {isDriver &&
                isConfirmed &&
                !isCancelled && (
                    <div className="mt-6 rounded-2xl border border-blue-200 bg-blue-50 p-5">

                        <h3 className="font-semibold text-gray-900">
                            Driver Controls
                        </h3>

                        <p className="mt-1 text-sm text-gray-600">
                            Manage the ride directly from your bookings.
                        </p>

                        <div className="mt-4">

                            {isScheduled && (
                                <button
                                    onClick={
                                        handleStartRide
                                    }
                                    className="inline-flex items-center gap-2 rounded-xl bg-blue-600 px-5 py-3 font-semibold text-white transition hover:bg-blue-700"
                                >
                                    <Play size={18} />
                                    Start Ride
                                </button>
                            )}

                            {isInProgress && (
                                <button
                                    onClick={
                                        handleEndRide
                                    }
                                    className="inline-flex items-center gap-2 rounded-xl bg-red-600 px-5 py-3 font-semibold text-white transition hover:bg-red-700"
                                >
                                    <Square size={18} />
                                    End Ride
                                </button>
                            )}

                            {awaitingPassengerConfirmation && (
                                <div className="rounded-xl bg-orange-100 p-4 text-sm font-medium text-orange-700">
                                    Ride ended. Waiting for passenger to confirm drop-off.
                                </div>
                            )}

                            {isCompleted && (
                                <div className="flex items-center gap-2 rounded-xl bg-green-100 p-4 text-sm font-semibold text-green-700">
                                    <CheckCircle size={18} />
                                    Ride completed.
                                </div>
                            )}

                        </div>

                    </div>
                )}

            {/* ================================================= */}
            {/* PASSENGER CONTROLS */}
            {/* ================================================= */}

            {!isDriver &&
                isConfirmed &&
                !isCancelled && (
                    <div className="mt-6 rounded-2xl border border-green-200 bg-green-50 p-5">

                        <h3 className="font-semibold text-gray-900">
                            Passenger Ride Status
                        </h3>

                        <p className="mt-1 text-sm text-gray-600">
                            Track your ride and confirm your drop-off here.
                        </p>

                        <div className="mt-4">

                            {isScheduled && (
                                <div className="rounded-xl bg-blue-100 p-4 text-sm font-medium text-blue-700">
                                    Waiting for the driver to start the ride.
                                </div>
                            )}

                            {isInProgress && (
                                <div className="rounded-xl bg-blue-100 p-4 text-sm font-medium text-blue-700">
                                    🚗 Your ride is currently in progress.
                                </div>
                            )}

                            {awaitingPassengerConfirmation && (
                                <button
                                    onClick={
                                        handleConfirmDropoff
                                    }
                                    className="inline-flex items-center gap-2 rounded-xl bg-green-600 px-5 py-3 font-semibold text-white transition hover:bg-green-700"
                                >
                                    <CheckCircle size={18} />
                                    Confirm Drop-off
                                </button>
                            )}

                            {isCompleted && (
                                <div className="flex items-center gap-2 rounded-xl bg-green-100 p-4 text-sm font-semibold text-green-700">
                                    <CheckCircle size={18} />
                                    Ride completed.
                                </div>
                            )}

                        </div>

                    </div>
                )}

            {/* ================================================= */}
            {/* Cancel Booking */}
            {/* ================================================= */}

            {isConfirmed &&
                !isInProgress &&
                !awaitingPassengerConfirmation &&
                !isCompleted && (
                    <div className="mt-6 flex justify-end">

                        <button
                            onClick={() =>
                                onCancel(booking)
                            }
                            className="rounded-xl bg-red-600 px-5 py-2.5 font-medium text-white transition hover:bg-red-700"
                        >
                            Cancel Booking
                        </button>

                    </div>
                )}

        </div>
    );
}
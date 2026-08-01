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
} from "lucide-react";

export default function BookingCard({
    booking,
    onCancel,
}) {
    const ride = booking.ride || {};

    const pickup =
        ride.pickup_location ??
        ride.pickup ??
        "Pickup";

    const destination =
        ride.dropoff_location ??
        ride.destination ??
        "Destination";

    const departure =
        ride.departure_time ||
        ride.departure_datetime;

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

    const status = booking.status;

    const confirmed =
        status === "CONFIRMED";

    const cancelled =
        status === "CANCELLED";

    return (
        <div className="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm transition hover:shadow-md">

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
                                <IndianRupee
                                    size={16}
                                />
                                ₹{price} / seat
                            </div>
                        )}

                    </div>

                </div>

                <div>
                    {confirmed && (
                        <span className="inline-flex items-center gap-2 rounded-full bg-green-100 px-4 py-2 text-sm font-semibold text-green-700">
                            <CheckCircle
                                size={16}
                            />
                            Confirmed
                        </span>
                    )}

                    {cancelled && (
                        <span className="inline-flex items-center gap-2 rounded-full bg-red-100 px-4 py-2 text-sm font-semibold text-red-700">
                            <XCircle
                                size={16}
                            />
                            Cancelled
                        </span>
                    )}

                    {!confirmed &&
                        !cancelled && (
                            <span className="inline-flex items-center gap-2 rounded-full bg-yellow-100 px-4 py-2 text-sm font-semibold text-yellow-700">
                                <Clock
                                    size={16}
                                />
                                {status}
                            </span>
                        )}
                </div>

            </div>

            <div className="mt-6 grid gap-4 md:grid-cols-2">

                <div className="space-y-3">

                    {driver && (
                        <div className="flex items-center gap-2">
                            <User
                                size={18}
                                className="text-blue-600"
                            />
                            <span>{driver}</span>
                        </div>
                    )}

                    {vehicle && (
                        <div className="flex items-center gap-2">
                            <Car
                                size={18}
                                className="text-blue-600"
                            />
                            <span>{vehicle}</span>
                        </div>
                    )}

                    {phone &&
                        confirmed && (
                            <div className="flex items-center gap-2">
                                <Phone
                                    size={18}
                                    className="text-blue-600"
                                />
                                <span>{phone}</span>
                            </div>
                        )}

                    {seats != null && (
                        <div className="flex items-center gap-2">
                            <Users
                                size={18}
                                className="text-blue-600"
                            />
                            <span>
                                Seats Left:{" "}
                                {seats}
                            </span>
                        </div>
                    )}

                </div>

                <div className="rounded-xl bg-gray-50 p-4">

                    <h3 className="mb-3 font-semibold text-gray-800">
                        Booking Timeline
                    </h3>

                    <div className="space-y-2 text-sm">

                        <div className="flex items-center gap-2 text-green-600">
                            <CheckCircle size={16} />
                            Requested
                        </div>

                        <div
                            className={`flex items-center gap-2 ${
                                confirmed
                                    ? "text-green-600"
                                    : "text-gray-400"
                            }`}
                        >
                            <CheckCircle size={16} />
                            Confirmed
                        </div>

                        <div className="flex items-center gap-2 text-gray-400">
                            <Clock size={16} />
                            Ride Started
                        </div>

                        <div className="flex items-center gap-2 text-gray-400">
                            <CheckCircle size={16} />
                            Completed
                        </div>

                    </div>

                </div>

            </div>

            {confirmed && (
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
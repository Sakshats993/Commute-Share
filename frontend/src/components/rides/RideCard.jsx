import {
    Clock,
    MapPin,
    Users,
    IndianRupee,
    Car,
    ArrowRight,
} from "lucide-react";

import useAuth from "../../hooks/useAuth";

export default function RideCard({
    ride,
    onView,
    onEdit,
    onDelete,
}) {
    const departure = new Date(ride.departure_time);

    const { user } = useAuth();

    const isOwner = user?.id === ride.driver_id;

    return (
        <div className="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm transition-all duration-200 hover:-translate-y-1 hover:shadow-lg">

            {/* Header */}
            <div className="flex items-start justify-between">

                <div className="flex items-center gap-3">

                    <div className="rounded-xl bg-blue-100 p-3">
                        <Car
                            size={22}
                            className="text-blue-600"
                        />
                    </div>

                    <div>
                        <p className="text-sm text-gray-500">
                            Ride
                        </p>

                        <h2 className="text-lg font-semibold text-gray-900">
                            {ride.pickup_location}
                        </h2>
                    </div>

                </div>

                <span
                    className={`rounded-full px-3 py-1 text-xs font-semibold capitalize ${
                        ride.status === "scheduled"
                            ? "bg-green-100 text-green-700"
                            : ride.status === "completed"
                            ? "bg-gray-100 text-gray-700"
                            : "bg-red-100 text-red-700"
                    }`}
                >
                    {ride.status}
                </span>

            </div>

            {/* Route */}

            <div className="my-6 rounded-xl bg-gray-50 p-4">

                <div className="flex items-center gap-2">
                    <MapPin
                        size={18}
                        className="text-green-600"
                    />

                    <span className="font-medium">
                        {ride.pickup_location}
                    </span>
                </div>

                <div className="ml-2 my-2 border-l-2 border-dashed border-gray-300 pl-4">
                    <ArrowRight
                        size={16}
                        className="text-gray-400"
                    />
                </div>

                <div className="flex items-center gap-2">
                    <MapPin
                        size={18}
                        className="text-red-600"
                    />

                    <span className="font-medium">
                        {ride.destination_location}
                    </span>
                </div>

            </div>

            {/* Ride Details */}

            <div className="grid grid-cols-1 gap-3 text-sm text-gray-700 sm:grid-cols-3">

                <div className="flex items-center gap-2">
                    <Clock size={16} />

                    <span>
                        {departure.toLocaleDateString()}{" "}
                        {departure.toLocaleTimeString([], {
                            hour: "2-digit",
                            minute: "2-digit",
                        })}
                    </span>
                </div>

                <div className="flex items-center gap-2">
                    <Users size={16} />

                    <span>
                        {ride.available_seats} / {ride.total_seats} Seats
                    </span>
                </div>

                <div className="flex items-center gap-2">
                    <IndianRupee size={16} />

                    <span className="font-semibold">
                        ₹{ride.price_per_seat}
                    </span>
                </div>

            </div>

            {/* Actions */}

            <div className="mt-6 flex flex-wrap gap-3">

                <button
                    onClick={() => onView(ride)}
                    className="rounded-lg bg-blue-600 px-4 py-2 font-medium text-white transition hover:bg-blue-700"
                >
                    View
                </button>

                {isOwner ? (
                    <>
                        <button
                            onClick={() => onEdit?.(ride)}
                            className="rounded-lg border border-green-600 px-4 py-2 font-medium text-green-600 transition hover:bg-green-600 hover:text-white"
                        >
                            Edit
                        </button>

                        <button
                            onClick={() => onDelete?.(ride)}
                            className="rounded-lg border border-red-600 px-4 py-2 font-medium text-red-600 transition hover:bg-red-600 hover:text-white"
                        >
                            Delete
                        </button>
                    </>
                ) : (
                    <button
                        onClick={() => onView(ride)}
                        className="rounded-lg border border-green-600 px-4 py-2 font-medium text-green-600 transition hover:bg-green-600 hover:text-white"
                    >
                        Book Ride
                    </button>
                )}

            </div>

        </div>
    );
}
import {
    Calendar,
    CheckCircle,
    XCircle,
} from "lucide-react";

export default function BookingCard({
    booking,
    onCancel,
}) {
    return (
        <div className="bg-white rounded-xl shadow p-6">

            <div className="flex justify-between">

                <h2 className="text-lg font-bold">
                    Booking #{booking.id}
                </h2>

                {booking.status ===
                "CONFIRMED" ? (
                    <span className="bg-green-100 text-green-700 px-3 py-1 rounded-full flex items-center gap-1">
                        <CheckCircle size={16} />
                        Confirmed
                    </span>
                ) : (
                    <span className="bg-red-100 text-red-700 px-3 py-1 rounded-full flex items-center gap-1">
                        <XCircle size={16} />
                        Cancelled
                    </span>
                )}

            </div>

            <div className="mt-5 space-y-2">

                <p>
                    <strong>Ride ID:</strong>{" "}
                    {booking.ride_id}
                </p>

                <p>
                    <strong>Booked On:</strong>{" "}
                    {new Date(
                        booking.created_at
                    ).toLocaleString()}
                </p>

            </div>

            {booking.status ===
                "CONFIRMED" && (
                <button
                    onClick={() =>
                        onCancel(booking)
                    }
                    className="mt-6 bg-red-600 text-white px-4 py-2 rounded-lg"
                >
                    Cancel Booking
                </button>
            )}

        </div>
    );
}
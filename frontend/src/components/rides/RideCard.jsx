import {
    Clock,
    MapPin,
    Users,
    IndianRupee,
} from "lucide-react";

export default function RideCard({
    ride,
    onView,
    onEdit,
    onDelete,
}) {
    return (
        <div className="bg-white rounded-xl shadow-lg p-6">
            <div className="flex justify-between">
                <div>
                    <h2 className="text-xl font-bold">
                        {ride.pickup_location}
                    </h2>

                    <p className="text-gray-500">
                        ↓
                    </p>

                    <h2 className="text-xl font-bold">
                        {ride.destination_location}
                    </h2>
                </div>

                <span className="bg-blue-100 text-blue-700 px-3 py-1 rounded-full h-fit">
                    {ride.status}
                </span>
            </div>

            <div className="mt-5 space-y-2">

                <div className="flex gap-2 items-center">
                    <Clock size={16}/>
                    {new Date(
                        ride.departure_time
                    ).toLocaleString()}
                </div>

                <div className="flex gap-2 items-center">
                    <Users size={16}/>
                    {ride.available_seats} / {ride.total_seats}
                </div>

                <div className="flex gap-2 items-center">
                    <IndianRupee size={16}/>
                    ₹{ride.price_per_seat}
                </div>

            </div>

            <div className="flex gap-3 mt-6">

                <button
                    onClick={() =>
                        onView(ride)
                    }
                    className="bg-blue-600 text-white px-4 py-2 rounded-lg"
                >
                    View
                </button>

                {onEdit && (
                    <button
                        onClick={() =>
                            onEdit(ride)
                        }
                        className="bg-green-600 text-white px-4 py-2 rounded-lg"
                    >
                        Edit
                    </button>
                )}

                {onDelete && (
                    <button
                        onClick={() =>
                            onDelete(ride)
                        }
                        className="bg-red-600 text-white px-4 py-2 rounded-lg"
                    >
                        Delete
                    </button>
                )}

            </div>
        </div>
    );
}
import { Pencil, Trash2 } from "lucide-react";

export default function VehicleCard({
    vehicle,
    onEdit,
    onDelete,
}) {
    return (
        <div className="bg-white rounded-xl shadow-md p-6">
            <div className="flex justify-between items-start">
                <div>
                    <h2 className="text-xl font-bold">
                        {vehicle.make} {vehicle.model}
                    </h2>

                    <p className="text-gray-500 mt-1">
                        {vehicle.registration_number}
                    </p>
                </div>

                <span
                    className={`px-3 py-1 rounded-full text-sm ${
                        vehicle.is_active
                            ? "bg-green-100 text-green-700"
                            : "bg-red-100 text-red-700"
                    }`}
                >
                    {vehicle.is_active
                        ? "Active"
                        : "Inactive"}
                </span>
            </div>

            <div className="mt-5 space-y-2">
                <p>
                    <strong>Color:</strong>{" "}
                    {vehicle.color}
                </p>

                <p>
                    <strong>Seats:</strong>{" "}
                    {vehicle.seating_capacity}
                </p>
            </div>

            <div className="flex gap-3 mt-6">
                <button
                    onClick={() => onEdit(vehicle)}
                    className="flex items-center gap-2 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
                >
                    <Pencil size={16} />
                    Edit
                </button>

                <button
                    onClick={() =>
                        onDelete(vehicle)
                    }
                    className="flex items-center gap-2 bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700"
                >
                    <Trash2 size={16} />
                    Delete
                </button>
            </div>
        </div>
    );
}
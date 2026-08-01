import {
    Car,
    Palette,
    Users,
    BadgeCheck,
    CircleOff,
    Pencil,
    Trash2,
} from "lucide-react";

export default function VehicleCard({
    vehicle,
    onEdit,
    onDelete,
}) {
    return (
        <div className="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm transition-all duration-200 hover:-translate-y-1 hover:shadow-lg">
            {/* Header */}
            <div className="flex items-start justify-between">
                <div className="flex items-center gap-4">
                    <div className="rounded-xl bg-blue-100 p-3">
                        <Car
                            size={24}
                            className="text-blue-600"
                        />
                    </div>

                    <div>
                        <h2 className="text-xl font-bold text-gray-900">
                            {vehicle.make} {vehicle.model}
                        </h2>

                        <p className="mt-1 text-sm text-gray-500">
                            {vehicle.registration_number}
                        </p>
                    </div>
                </div>

                <span
                    className={`flex items-center gap-1 rounded-full px-3 py-1 text-sm font-medium ${
                        vehicle.is_active
                            ? "bg-green-100 text-green-700"
                            : "bg-red-100 text-red-700"
                    }`}
                >
                    {vehicle.is_active ? (
                        <>
                            <BadgeCheck size={15} />
                            Active
                        </>
                    ) : (
                        <>
                            <CircleOff size={15} />
                            Inactive
                        </>
                    )}
                </span>
            </div>

            {/* Details */}
            <div className="mt-6 grid gap-4 sm:grid-cols-2">
                <div className="rounded-xl bg-gray-50 p-4">
                    <div className="mb-2 flex items-center gap-2">
                        <Palette
                            size={18}
                            className="text-blue-600"
                        />
                        <span className="text-sm font-medium text-gray-500">
                            Color
                        </span>
                    </div>

                    <p className="font-semibold text-gray-900">
                        {vehicle.color}
                    </p>
                </div>

                <div className="rounded-xl bg-gray-50 p-4">
                    <div className="mb-2 flex items-center gap-2">
                        <Users
                            size={18}
                            className="text-blue-600"
                        />
                        <span className="text-sm font-medium text-gray-500">
                            Seating Capacity
                        </span>
                    </div>

                    <p className="font-semibold text-gray-900">
                        {vehicle.seating_capacity} Seats
                    </p>
                </div>
            </div>

            {/* Actions */}
            <div className="mt-6 flex flex-wrap gap-3">
                <button
                    onClick={() => onEdit(vehicle)}
                    className="flex items-center gap-2 rounded-xl bg-blue-600 px-5 py-2.5 font-medium text-white transition hover:bg-blue-700"
                >
                    <Pencil size={16} />
                    Edit
                </button>

                <button
                    onClick={() => onDelete(vehicle)}
                    className="flex items-center gap-2 rounded-xl border border-red-600 px-5 py-2.5 font-medium text-red-600 transition hover:bg-red-600 hover:text-white"
                >
                    <Trash2 size={16} />
                    Delete
                </button>
            </div>
        </div>
    );
}
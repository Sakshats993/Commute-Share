import VehicleCard from "./VehicleCard";

export default function VehicleList({
    vehicles,
    onEdit,
    onDelete,
}) {
    if (!vehicles || vehicles.length === 0) {
        return (
            <div className="rounded-2xl border border-dashed border-gray-300 bg-white px-8 py-20 text-center shadow-sm">
                <div className="mx-auto mb-5 flex h-16 w-16 items-center justify-center rounded-full bg-blue-100 text-3xl">
                    🚘
                </div>

                <h2 className="text-2xl font-semibold text-gray-900">
                    No Vehicles Found
                </h2>

                <p className="mt-2 text-gray-500">
                    Register your first vehicle to start creating rides.
                </p>
            </div>
        );
    }

    return (
        <>
            <div className="mb-5 flex items-center justify-between">
                <h2 className="text-xl font-semibold text-gray-900">
                    Registered Vehicles
                </h2>

                <span className="rounded-full bg-blue-100 px-3 py-1 text-sm font-medium text-blue-700">
                    {vehicles.length}{" "}
                    {vehicles.length === 1
                        ? "Vehicle"
                        : "Vehicles"}
                </span>
            </div>

            <div className="grid gap-6 lg:grid-cols-2">
                {vehicles.map((vehicle) => (
                    <VehicleCard
                        key={vehicle.id}
                        vehicle={vehicle}
                        onEdit={onEdit}
                        onDelete={onDelete}
                    />
                ))}
            </div>
        </>
    );
}
import VehicleCard from "./VehicleCard";

export default function VehicleList({
    vehicles,
    onEdit,
    onDelete,
}) {
    return (
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {vehicles.map((vehicle) => (
                <VehicleCard
                    key={vehicle.id}
                    vehicle={vehicle}
                    onEdit={onEdit}
                    onDelete={onDelete}
                />
            ))}
        </div>
    );
}
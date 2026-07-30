import RideCard from "./RideCard";

export default function RideList({
    rides,
    onView,
    onEdit,
    onDelete,
}) {
    if (rides.length === 0) {
        return (
            <div className="text-center py-20 text-gray-500">
                No rides available.
            </div>
        );
    }

    return (
        <div className="grid gap-6 lg:grid-cols-2">
            {rides.map((ride) => (
                <RideCard
                    key={ride.id}
                    ride={ride}
                    onView={onView}
                    onEdit={onEdit}
                    onDelete={onDelete}
                />
            ))}
        </div>
    );
}
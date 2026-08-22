import RideCard from "./RideCard";
import useAuth from "../../hooks/useAuth";

export default function RideList({
    rides,
    onView,
    onEdit,
    onDelete,
}) {
    const { user } = useAuth();

    if (!rides || rides.length === 0) {
        return (
            <div className="rounded-2xl border border-dashed border-gray-300 bg-white py-20 px-8 text-center shadow-sm">
                <div className="mx-auto mb-5 flex h-16 w-16 items-center justify-center rounded-full bg-blue-100">
                    🚗
                </div>

                <h2 className="text-2xl font-semibold text-gray-900">
                    No rides found
                </h2>

                <p className="mt-2 text-gray-500">
                    There are currently no rides matching your search.
                    Create a ride or adjust your filters.
                </p>
            </div>
        );
    }

    const isDriver = user?.role?.toLowerCase() === "driver";

    const myRides = rides.filter(
        (ride) => ride.driver_id === user?.id
    );

    const otherRides = rides.filter(
        (ride) => ride.driver_id !== user?.id
    );

    return (
        <>
            {/* DRIVER VIEW */}
            {isDriver ? (
                <>
                    {/* My Rides */}
                    <div className="mb-10">
                        <div className="mb-5 flex items-center justify-between">
                            <h2 className="text-2xl font-bold text-gray-900">
                                🚗 My Rides
                            </h2>

                            <span className="rounded-full bg-green-100 px-3 py-1 text-sm font-medium text-green-700">
                                {myRides.length}{" "}
                                {myRides.length === 1
                                    ? "Ride"
                                    : "Rides"}
                            </span>
                        </div>

                        {myRides.length === 0 ? (
                            <div className="rounded-xl border border-dashed border-gray-300 bg-white p-10 text-center text-gray-500">
                                You haven't created any rides yet.
                            </div>
                        ) : (
                            <div className="grid gap-6 xl:grid-cols-2">
                                {myRides.map((ride) => (
                                    <RideCard
                                        key={ride.id}
                                        ride={ride}
                                        onView={onView}
                                        onEdit={onEdit}
                                        onDelete={onDelete}
                                    />
                                ))}
                            </div>
                        )}
                    </div>

                    {/* Other Rides */}
                    <div>
                        <div className="mb-5 flex items-center justify-between">
                            <h2 className="text-2xl font-bold text-gray-900">
                                🌍 Available Rides
                            </h2>

                            <span className="rounded-full bg-blue-100 px-3 py-1 text-sm font-medium text-blue-700">
                                {otherRides.length}{" "}
                                {otherRides.length === 1
                                    ? "Ride"
                                    : "Rides"}
                            </span>
                        </div>

                        {otherRides.length === 0 ? (
                            <div className="rounded-xl border border-dashed border-gray-300 bg-white p-10 text-center text-gray-500">
                                No other rides available.
                            </div>
                        ) : (
                            <div className="grid gap-6 xl:grid-cols-2">
                                {otherRides.map((ride) => (
                                    <RideCard
                                        key={ride.id}
                                        ride={ride}
                                        onView={onView}
                                        onEdit={onEdit}
                                        onDelete={onDelete}
                                    />
                                ))}
                            </div>
                        )}
                    </div>
                </>
            ) : (
                <>
                    {/* PASSENGER VIEW */}
                    <div className="mb-5 flex items-center justify-between">
                        <h2 className="text-2xl font-bold text-gray-900">
                            🌍 Available Rides
                        </h2>

                        <span className="rounded-full bg-blue-100 px-3 py-1 text-sm font-medium text-blue-700">
                            {rides.length}{" "}
                            {rides.length === 1 ? "Ride" : "Rides"}
                        </span>
                    </div>

                    <div className="grid gap-6 xl:grid-cols-2">
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
                </>
            )}
        </>
    );
}
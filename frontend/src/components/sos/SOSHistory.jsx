export default function SOSHistory({
    events,
    onView,
}) {
    if (events.length === 0) {
        return (
            <div className="text-center py-10 text-gray-500">
                No SOS events found.
            </div>
        );
    }

    return (
        <div className="space-y-4">
            {events.map((event) => (
                <div
                    key={event.id}
                    className="bg-white rounded-xl shadow border p-5 flex justify-between items-start"
                >
                    <div>
                        <h3 className="font-semibold text-lg">
                            {event.emergency_type}
                        </h3>

                        {event.description && (
                            <p className="text-gray-600 mt-2">
                                {event.description}
                            </p>
                        )}

                        <div className="mt-3 text-sm text-gray-500 space-y-1">
                            <p>
                                Ride ID: {event.ride_id}
                            </p>

                            <p>
                                Status: {event.status}
                            </p>

                            <p>
                                {new Date(
                                    event.created_at
                                ).toLocaleString()}
                            </p>
                        </div>
                    </div>

                    <button
                        onClick={() => onView(event.id)}
                        className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg"
                    >
                        View
                    </button>
                </div>
            ))}
        </div>
    );
}
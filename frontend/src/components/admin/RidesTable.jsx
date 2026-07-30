export default function RidesTable({
    rides,
}) {
    return (
        <div className="bg-white rounded-xl shadow border overflow-x-auto">

            <table className="min-w-full">

                <thead className="bg-gray-100">
                    <tr>
                        <th className="p-4 text-left">ID</th>
                        <th className="p-4 text-left">Driver</th>
                        <th className="p-4 text-left">Pickup</th>
                        <th className="p-4 text-left">Destination</th>
                    </tr>
                </thead>

                <tbody>

                    {rides.map((ride) => (
                        <tr
                            key={ride.id}
                            className="border-t"
                        >
                            <td className="p-4">
                                {ride.id}
                            </td>

                            <td className="p-4">
                                {ride.driver_id}
                            </td>

                            <td className="p-4">
                                {ride.pickup_location}
                            </td>

                            <td className="p-4">
                                {ride.destination_location}
                            </td>
                        </tr>
                    ))}

                </tbody>

            </table>

        </div>
    );
}
export default function BookingsTable({
    bookings,
}) {
    return (
        <div className="bg-white rounded-xl shadow border overflow-x-auto">

            <table className="min-w-full">

                <thead className="bg-gray-100">

                    <tr>
                        <th className="p-4 text-left">ID</th>
                        <th className="p-4 text-left">Ride</th>
                        <th className="p-4 text-left">Passenger</th>
                        <th className="p-4 text-left">Status</th>
                    </tr>

                </thead>

                <tbody>

                    {bookings.map((booking) => (
                        <tr
                            key={booking.id}
                            className="border-t"
                        >
                            <td className="p-4">
                                {booking.id}
                            </td>

                            <td className="p-4">
                                {booking.ride_id}
                            </td>

                            <td className="p-4">
                                {booking.passenger_id}
                            </td>

                            <td className="p-4">
                                {booking.status}
                            </td>
                        </tr>
                    ))}

                </tbody>

            </table>

        </div>
    );
}
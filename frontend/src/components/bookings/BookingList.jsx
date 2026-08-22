import BookingCard from "./BookingCard";

export default function BookingList({
    bookings,
    onCancel,
}) {
    if (!bookings || bookings.length === 0) {
        return (
            <div className="rounded-2xl border border-dashed border-gray-300 bg-white px-8 py-20 text-center shadow-sm">
                <div className="mx-auto mb-5 flex h-16 w-16 items-center justify-center rounded-full bg-blue-100 text-3xl">
                    📅
                </div>

                <h2 className="text-2xl font-semibold text-gray-900">
                    No Bookings Yet
                </h2>

                <p className="mt-2 text-gray-500">
                    You haven't booked any rides yet. Browse available rides and
                    reserve your first trip.
                </p>
            </div>
        );
    }

    return (
        <>
            <div className="mb-6 flex items-center justify-between">
                <h2 className="text-xl font-semibold text-gray-900">
                    Booking History
                </h2>

                <span className="rounded-full bg-blue-100 px-3 py-1 text-sm font-medium text-blue-700">
                    {bookings.length}{" "}
                    {bookings.length === 1 ? "Booking" : "Bookings"}
                </span>
            </div>

            <div className="grid gap-6 lg:grid-cols-2">
                {bookings.map((booking) => (
                    <BookingCard
                        key={booking.id}
                        booking={booking}
                        onCancel={onCancel}
                    />
                ))}
            </div>
        </>
    );
}
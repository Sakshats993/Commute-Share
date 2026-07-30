import BookingCard from "./BookingCard";

export default function BookingList({
    bookings,
    onCancel,
}) {
    if (bookings.length === 0) {
        return (
            <div className="text-center py-20 text-gray-500">
                No bookings found.
            </div>
        );
    }

    return (
        <div className="grid lg:grid-cols-2 gap-6">

            {bookings.map((booking) => (
                <BookingCard
                    key={booking.id}
                    booking={booking}
                    onCancel={onCancel}
                />
            ))}

        </div>
    );
}
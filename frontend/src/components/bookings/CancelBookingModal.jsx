export default function CancelBookingModal({
    booking,
    onConfirm,
    onCancel,
}) {
    if (!booking) return null;

    return (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
            <div className="bg-white rounded-xl shadow-lg w-full max-w-md p-6">
                <h2 className="text-2xl font-bold">
                    Cancel Booking
                </h2>

                <p className="mt-4 text-gray-600">
                    Are you sure you want to cancel this booking?
                </p>

                <div className="flex justify-end gap-3 mt-8">
                    <button
                        onClick={onCancel}
                        className="px-4 py-2 rounded-lg border border-gray-300 hover:bg-gray-100"
                    >
                        No
                    </button>

                    <button
                        onClick={() => onConfirm(booking.id)}
                        className="px-4 py-2 rounded-lg bg-red-600 text-white hover:bg-red-700"
                    >
                        Yes, Cancel
                    </button>
                </div>
            </div>
        </div>
    );
}
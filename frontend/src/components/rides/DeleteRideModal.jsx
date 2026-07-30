export default function DeleteRideModal({
    ride,
    onConfirm,
    onCancel,
}) {
    if (!ride) return null;

    return (
        <div className="fixed inset-0 bg-black/50 flex justify-center items-center">
            <div className="bg-white rounded-xl p-6 w-full max-w-md">
                <h2 className="text-xl font-bold">
                    Delete Ride
                </h2>

                <p className="mt-4">
                    Are you sure you want to delete
                    this ride?
                </p>

                <div className="flex justify-end gap-3 mt-6">
                    <button
                        onClick={onCancel}
                        className="bg-gray-300 px-4 py-2 rounded-lg"
                    >
                        Cancel
                    </button>

                    <button
                        onClick={() =>
                            onConfirm(ride.id)
                        }
                        className="bg-red-600 text-white px-4 py-2 rounded-lg"
                    >
                        Delete
                    </button>
                </div>
            </div>
        </div>
    );
}
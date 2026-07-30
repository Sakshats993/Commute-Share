export default function DeleteVehicleModal({
    vehicle,
    onConfirm,
    onCancel,
}) {
    if (!vehicle) return null;

    return (
        <div className="fixed inset-0 bg-black/40 flex items-center justify-center">
            <div className="bg-white rounded-xl p-6 w-full max-w-md">
                <h2 className="text-xl font-bold">
                    Delete Vehicle
                </h2>

                <p className="mt-4">
                    Are you sure you want to delete
                    <strong>
                        {" "}
                        {vehicle.make}{" "}
                        {vehicle.model}
                    </strong>
                    ?
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
                            onConfirm(vehicle.id)
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
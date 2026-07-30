export default function RatingCard({
    rating,
    onEdit,
    onDelete,
}) {
    return (
        <div className="bg-white rounded-xl shadow border p-5">

            <div className="flex justify-between items-start">

                <div>

                    <div className="flex items-center gap-2">

                        <span className="text-yellow-500 text-xl">
                            {"★".repeat(rating.rating)}
                        </span>

                        <span className="font-semibold">
                            {rating.rating}/5
                        </span>

                    </div>

                    {rating.review && (
                        <p className="mt-3 text-gray-700">
                            {rating.review}
                        </p>
                    )}

                    <div className="mt-4 text-sm text-gray-500 space-y-1">

                        <p>
                            Ride ID: {rating.ride_id}
                        </p>

                        <p>
                            Reviewer ID: {rating.reviewer_id}
                        </p>

                        <p>
                            {new Date(
                                rating.created_at
                            ).toLocaleString()}
                        </p>

                    </div>

                </div>

                <div className="flex gap-2">

                    <button
                        onClick={() => onEdit(rating)}
                        className="px-3 py-2 rounded-lg bg-blue-600 text-white hover:bg-blue-700"
                    >
                        Edit
                    </button>

                    <button
                        onClick={() => onDelete(rating)}
                        className="px-3 py-2 rounded-lg bg-red-600 text-white hover:bg-red-700"
                    >
                        Delete
                    </button>

                </div>

            </div>

        </div>
    );
}
export default function RatingCard({
    rating,
    onEdit,
    onDelete,
}) {
    const reviewerRole =
        rating.reviewer_role === "driver"
            ? "Driver"
            : "Passenger";

    return (
        <div className="bg-white rounded-2xl border border-gray-200 shadow-sm p-6">
            <div className="flex justify-between items-start gap-6">

                <div className="flex-1">

                    {/* Reviewer */}
                    <div className="mb-3">
                        <p className="text-sm text-gray-500">
                            Rating from {reviewerRole}
                        </p>

                        <p className="text-lg font-semibold text-gray-900">
                            {rating.reviewer_name}
                        </p>
                    </div>

                    {/* Rating */}
                    <div className="flex items-center gap-2">
                        <span className="text-yellow-500 text-xl">
                            {"★".repeat(rating.rating)}
                            {"☆".repeat(5 - rating.rating)}
                        </span>

                        <span className="font-semibold text-gray-700">
                            {rating.rating}/5
                        </span>
                    </div>

                    {/* Review */}
                    {rating.review && (
                        <p className="mt-4 text-gray-700 leading-relaxed">
                            "{rating.review}"
                        </p>
                    )}

                    {/* Date */}
                    <p className="mt-4 text-sm text-gray-400">
                        {new Date(
                            rating.created_at
                        ).toLocaleString()}
                    </p>
                </div>

                {/* Actions */}
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
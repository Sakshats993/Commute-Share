import RatingCard from "./RatingCard";

export default function RatingList({
    ratings,
    onEdit,
    onDelete,
}) {
    if (ratings.length === 0) {
        return (
            <div className="text-center py-16 text-gray-500">
                No ratings found.
            </div>
        );
    }

    return (
        <div className="space-y-4">
            {ratings.map((rating) => (
                <RatingCard
                    key={rating.id}
                    rating={rating}
                    onEdit={onEdit}
                    onDelete={onDelete}
                />
            ))}
        </div>
    );
}
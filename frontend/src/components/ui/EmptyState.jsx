export default function EmptyState({
    title,
    description,
}) {
    return (
        <div className="bg-white rounded-xl shadow p-10 text-center">
            <h2 className="text-xl font-semibold mb-2">
                {title}
            </h2>

            <p className="text-gray-500">
                {description}
            </p>
        </div>
    );
}
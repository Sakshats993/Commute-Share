export default function DashboardCard({
    title,
    value,
    description,
}) {
    return (
        <div className="bg-white rounded-xl shadow p-6">
            <h3 className="text-gray-500 text-sm">
                {title}
            </h3>

            <h2 className="text-3xl font-bold mt-2">
                {value}
            </h2>

            {description && (
                <p className="text-gray-500 mt-3">
                    {description}
                </p>
            )}
        </div>
    );
}
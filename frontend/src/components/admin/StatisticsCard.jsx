export default function StatisticsCard({
    title,
    value,
}) {
    return (
        <div className="bg-white rounded-xl shadow border p-6">

            <h3 className="text-gray-500 text-sm font-medium">
                {title}
            </h3>

            <p className="mt-3 text-3xl font-bold">
                {value}
            </p>

        </div>
    );
}
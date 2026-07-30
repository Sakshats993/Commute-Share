import StatisticsCard from "./StatisticsCard";

export default function AdminStatistics({
    statistics,
}) {
    if (!statistics) return null;

    return (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">

            <StatisticsCard
                title="Total Users"
                value={statistics.total_users}
            />

            <StatisticsCard
                title="Active Users"
                value={statistics.active_users}
            />

            <StatisticsCard
                title="Total Rides"
                value={statistics.total_rides}
            />

            <StatisticsCard
                title="Total Bookings"
                value={statistics.total_bookings}
            />

        </div>
    );
}
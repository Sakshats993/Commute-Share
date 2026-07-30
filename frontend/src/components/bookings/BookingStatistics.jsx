import DashboardCard from "../common/DashboardCard";

export default function BookingStatistics({ statistics }) {
    if (!statistics) return null;

    return (
        <div className="grid md:grid-cols-3 gap-6 mb-8">
            <DashboardCard
                title="Total Bookings"
                value={statistics.total_bookings}
            />

            <DashboardCard
                title="Confirmed"
                value={statistics.confirmed_bookings}
            />

            <DashboardCard
                title="Cancelled"
                value={statistics.cancelled_bookings}
            />
        </div>
    );
}
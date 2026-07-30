import { useEffect } from "react";
import toast from "react-hot-toast";

import Layout from "../components/ui/Layout";
import LoadingSpinner from "../components/ui/LoadingSpinner";

import AdminStatistics from "../components/admin/AdminStatistics";
import UsersTable from "../components/admin/UsersTable";
import RidesTable from "../components/admin/RidesTable";
import BookingsTable from "../components/admin/BookingsTable";

import useAdmin from "../hooks/useAdmin";

export default function AdminDashboardPage() {
    const {
        statistics,
        users,
        rides,
        bookings,
        loading,
        loadDashboard,
        activate,
        deactivate,
    } = useAdmin();

    useEffect(() => {
        loadDashboard();
    }, []);

    async function handleActivate(id) {
        try {
            await activate(id);

            toast.success(
                "User activated successfully."
            );
        } catch (error) {
            toast.error(
                error.response?.data?.detail ??
                    "Unable to activate user."
            );
        }
    }

    async function handleDeactivate(id) {
        try {
            await deactivate(id);

            toast.success(
                "User deactivated successfully."
            );
        } catch (error) {
            toast.error(
                error.response?.data?.detail ??
                    "Unable to deactivate user."
            );
        }
    }

    if (loading) {
        return (
            <Layout>
                <LoadingSpinner />
            </Layout>
        );
    }

    return (
        <Layout>
            <div className="space-y-8">

                <h1 className="text-3xl font-bold">
                    Admin Dashboard
                </h1>

                <AdminStatistics
                    statistics={statistics}
                />

                <section className="space-y-4">

                    <h2 className="text-2xl font-semibold">
                        Users
                    </h2>

                    <UsersTable
                        users={users}
                        onActivate={handleActivate}
                        onDeactivate={handleDeactivate}
                    />

                </section>

                <section className="space-y-4">

                    <h2 className="text-2xl font-semibold">
                        Rides
                    </h2>

                    <RidesTable
                        rides={rides}
                    />

                </section>

                <section className="space-y-4">

                    <h2 className="text-2xl font-semibold">
                        Bookings
                    </h2>

                    <BookingsTable
                        bookings={bookings}
                    />

                </section>

            </div>
        </Layout>
    );
}
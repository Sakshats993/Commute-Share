import Layout from "../components/ui/Layout";
import DashboardCard from "../components/common/DashboardCard";
import useAuth from "../hooks/useAuth";

export default function ProfilePage() {
    const { user } = useAuth();

    return (
        <Layout>
            <div className="space-y-6">

                <h1 className="text-3xl font-bold">
                    My Profile
                </h1>

                <DashboardCard>

                    <div className="space-y-4">

                        <div>
                            <h2 className="text-gray-500 text-sm">
                                Full Name
                            </h2>

                            <p className="text-lg font-semibold">
                                {user?.full_name || "-"}
                            </p>
                        </div>

                        <div>
                            <h2 className="text-gray-500 text-sm">
                                Email
                            </h2>

                            <p className="text-lg">
                                {user?.email || "-"}
                            </p>
                        </div>

                        <div>
                            <h2 className="text-gray-500 text-sm">
                                Phone Number
                            </h2>

                            <p className="text-lg">
                                {user?.phone_number || "-"}
                            </p>
                        </div>

                        <div>
                            <h2 className="text-gray-500 text-sm">
                                Role
                            </h2>

                            <p className="text-lg capitalize">
                                {user?.role || "-"}
                            </p>
                        </div>

                        <div>
                            <h2 className="text-gray-500 text-sm">
                                Bio
                            </h2>

                            <p className="text-lg">
                                {user?.bio || "No bio added."}
                            </p>
                        </div>

                    </div>

                </DashboardCard>

            </div>
        </Layout>
    );
}
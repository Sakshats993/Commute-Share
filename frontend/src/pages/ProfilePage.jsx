import {
    Mail,
    Phone,
    Shield,
    User,
    FileText,
} from "lucide-react";

import DashboardCard from "../components/common/DashboardCard";
import Layout from "../components/ui/Layout";
import useAuth from "../hooks/useAuth";

export default function ProfilePage() {
    const { user } = useAuth();

    const profileItems = [
        {
            icon: <User size={18} className="text-blue-600" />,
            label: "Full Name",
            value: user?.full_name || "-",
        },
        {
            icon: <Mail size={18} className="text-blue-600" />,
            label: "Email",
            value: user?.email || "-",
        },
        {
            icon: <Phone size={18} className="text-blue-600" />,
            label: "Phone Number",
            value: user?.phone_number || "-",
        },
        {
            icon: <Shield size={18} className="text-blue-600" />,
            label: "Role",
            value: user?.role || "-",
        },
        {
            icon: <FileText size={18} className="text-blue-600" />,
            label: "Bio",
            value: user?.bio || "No bio added yet.",
        },
    ];

    return (
        <Layout>
            <div className="space-y-8">
                <div className="rounded-2xl bg-gradient-to-r from-blue-600 to-indigo-600 p-8 text-white shadow-lg">
                    <div className="flex items-center gap-5">
                        <div className="flex h-20 w-20 items-center justify-center rounded-full bg-white text-3xl font-bold text-blue-600">
                            {user?.full_name?.charAt(0)?.toUpperCase() || "U"}
                        </div>

                        <div>
                            <h1 className="text-3xl font-bold">
                                {user?.full_name || "User"}
                            </h1>

                            <p className="mt-1 text-blue-100">
                                {user?.email}
                            </p>

                            <span className="mt-3 inline-block rounded-full bg-white/20 px-3 py-1 text-sm capitalize">
                                {user?.role}
                            </span>
                        </div>
                    </div>
                </div>

                <DashboardCard>
                    <div className="space-y-6">
                        <h2 className="text-xl font-semibold text-gray-900">
                            Personal Information
                        </h2>

                        <div className="grid gap-5 md:grid-cols-2">
                            {profileItems.map((item) => (
                                <div
                                    key={item.label}
                                    className="rounded-xl border border-gray-200 p-4 transition hover:border-blue-400 hover:shadow-md"
                                >
                                    <div className="mb-2 flex items-center gap-2">
                                        {item.icon}

                                        <span className="text-sm font-medium text-gray-500">
                                            {item.label}
                                        </span>
                                    </div>

                                    <p className="break-words text-lg font-semibold text-gray-900 capitalize">
                                        {item.value}
                                    </p>
                                </div>
                            ))}
                        </div>
                    </div>
                </DashboardCard>
            </div>
        </Layout>
    );
}
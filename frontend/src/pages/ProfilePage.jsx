import {
    Award,
    BadgeCheck,
    Calendar,
    FileText,
    Mail,
    Phone,
    Shield,
    Star,
    User,
} from "lucide-react";

import Layout from "../components/ui/Layout";
import useAuth from "../hooks/useAuth";

export default function ProfilePage() {
    const { user } = useAuth();

    if (!user) {
        return (
            <Layout>
                <div className="flex justify-center py-24">
                    <p className="text-gray-500">
                        Unable to load profile.
                    </p>
                </div>
            </Layout>
        );
    }

    const role = String(user.role || "")
        .toLowerCase();

    const roleLabel =
        role.charAt(0).toUpperCase() +
        role.slice(1);

    const initials =
        user.full_name
            ?.split(" ")
            .map((name) => name[0])
            .join("")
            .slice(0, 2)
            .toUpperCase() || "U";

    const joinedDate = user.created_at
        ? new Date(
              user.created_at
          ).toLocaleDateString("en-IN", {
              day: "numeric",
              month: "long",
              year: "numeric",
          })
        : "-";

    const profileItems = [
        {
            icon: (
                <User
                    size={18}
                    className="text-blue-600"
                />
            ),
            label: "Full Name",
            value: user.full_name || "-",
        },
        {
            icon: (
                <Mail
                    size={18}
                    className="text-blue-600"
                />
            ),
            label: "Email",
            value: user.email || "-",
        },
        {
            icon: (
                <Phone
                    size={18}
                    className="text-blue-600"
                />
            ),
            label: "Phone Number",
            value:
                user.phone_number ||
                "Not provided",
        },
        {
            icon: (
                <Shield
                    size={18}
                    className="text-blue-600"
                />
            ),
            label: "Role",
            value: roleLabel || "-",
        },
        {
            icon: (
                <FileText
                    size={18}
                    className="text-blue-600"
                />
            ),
            label: "Bio",
            value:
                user.bio ||
                "No bio added yet.",
        },
        {
            icon: (
                <Calendar
                    size={18}
                    className="text-blue-600"
                />
            ),
            label: "Member Since",
            value: joinedDate,
        },
    ];

    return (
        <Layout>
            <div className="space-y-8">

                {/* ================================================== */}
                {/* Profile Header */}
                {/* ================================================== */}

                <div className="overflow-hidden rounded-3xl bg-gradient-to-r from-blue-600 via-blue-700 to-indigo-700 p-8 text-white shadow-lg">

                    <div className="flex flex-col gap-6 sm:flex-row sm:items-center">

                        {/* Profile Image / Initials */}
                        <div className="flex h-24 w-24 shrink-0 items-center justify-center overflow-hidden rounded-full border-4 border-white/30 bg-white text-3xl font-bold text-blue-600 shadow-lg">

                            {user.profile_image ? (
                                <img
                                    src={user.profile_image}
                                    alt={user.full_name}
                                    className="h-full w-full object-cover"
                                />
                            ) : (
                                initials
                            )}

                        </div>

                        {/* User Information */}
                        <div className="flex-1">

                            <div className="flex flex-wrap items-center gap-3">

                                <h1 className="text-3xl font-bold">
                                    {user.full_name}
                                </h1>

                                {user.is_verified && (
                                    <span className="inline-flex items-center gap-1 rounded-full bg-white/20 px-3 py-1 text-sm font-medium">
                                        <BadgeCheck
                                            size={16}
                                        />
                                        Verified
                                    </span>
                                )}

                            </div>

                            <p className="mt-2 text-blue-100">
                                {user.email}
                            </p>

                            <div className="mt-4 flex flex-wrap gap-3">

                                <span className="rounded-full bg-white/20 px-4 py-1.5 text-sm font-medium capitalize">
                                    {roleLabel}
                                </span>

                                <span
                                    className={`rounded-full px-4 py-1.5 text-sm font-medium ${
                                        user.is_active
                                            ? "bg-green-400/20 text-green-100"
                                            : "bg-red-400/20 text-red-100"
                                    }`}
                                >
                                    {user.is_active
                                        ? "Active Account"
                                        : "Inactive Account"}
                                </span>

                            </div>

                        </div>

                    </div>

                </div>

                {/* ================================================== */}
                {/* Reputation */}
                {/* ================================================== */}

                <div className="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm">

                    <div className="space-y-6">

                        <div>
                            <h2 className="text-xl font-semibold text-gray-900">
                                Reputation & Activity
                            </h2>

                            <p className="mt-1 text-sm text-gray-500">
                                Your CommuteShare performance and reputation.
                            </p>
                        </div>

                        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">

                            {/* Rating */}
                            <div className="rounded-2xl border border-gray-200 bg-gray-50 p-5">

                                <div className="flex items-center gap-2 text-gray-500">
                                    <Star
                                        size={18}
                                        className="fill-yellow-400 text-yellow-400"
                                    />
                                    <span className="text-sm font-medium">
                                        Average Rating
                                    </span>
                                </div>

                                <p className="mt-3 text-3xl font-bold text-gray-900">
                                    {Number(
                                        user.average_rating ?? 0
                                    ).toFixed(1)}
                                </p>

                                <p className="mt-1 text-sm text-gray-500">
                                    {user.review_count ?? 0}{" "}
                                    {user.review_count === 1
                                        ? "review"
                                        : "reviews"}
                                </p>

                            </div>

                            {/* Trust Score */}
                            <div className="rounded-2xl border border-gray-200 bg-gray-50 p-5">

                                <div className="flex items-center gap-2 text-gray-500">
                                    <Award
                                        size={18}
                                        className="text-blue-600"
                                    />
                                    <span className="text-sm font-medium">
                                        Trust Score
                                    </span>
                                </div>

                                <p className="mt-3 text-3xl font-bold text-gray-900">
                                    {Number(
                                        user.trust_score ?? 0
                                    ).toFixed(0)}
                                </p>

                                <p className="mt-1 text-sm text-gray-500">
                                    Community trust
                                </p>

                            </div>

                            {/* Completed Rides */}
                            <div className="rounded-2xl border border-gray-200 bg-gray-50 p-5">

                                <div className="flex items-center gap-2 text-gray-500">
                                    <Shield
                                        size={18}
                                        className="text-green-600"
                                    />
                                    <span className="text-sm font-medium">
                                        Completed Rides
                                    </span>
                                </div>

                                <p className="mt-3 text-3xl font-bold text-gray-900">
                                    {user.completed_rides ?? 0}
                                </p>

                                <p className="mt-1 text-sm text-gray-500">
                                    Successfully completed
                                </p>

                            </div>

                            {/* Reviews */}
                            <div className="rounded-2xl border border-gray-200 bg-gray-50 p-5">

                                <div className="flex items-center gap-2 text-gray-500">
                                    <Star
                                        size={18}
                                        className="text-purple-600"
                                    />
                                    <span className="text-sm font-medium">
                                        Reviews Received
                                    </span>
                                </div>

                                <p className="mt-3 text-3xl font-bold text-gray-900">
                                    {user.review_count ?? 0}
                                </p>

                                <p className="mt-1 text-sm text-gray-500">
                                    From the community
                                </p>

                            </div>

                        </div>
                                    
                    </div>

                </div>

                {/* ================================================== */}
                {/* Personal Information */}
                {/* ================================================== */}

                <div className="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm">

                    <div className="space-y-6">

                        <div>
                            <h2 className="text-xl font-semibold text-gray-900">
                                Personal Information
                            </h2>

                            <p className="mt-1 text-sm text-gray-500">
                                Your account and contact information.
                            </p>
                        </div>

                        <div className="grid gap-5 md:grid-cols-2">

                            {profileItems.map((item) => (
                                <div
                                    key={item.label}
                                    className="rounded-xl border border-gray-200 p-5 transition hover:border-blue-400 hover:shadow-md"
                                >
                                    <div className="mb-2 flex items-center gap-2">
                                        {item.icon}

                                        <span className="text-sm font-medium text-gray-500">
                                            {item.label}
                                        </span>
                                    </div>

                                    <p className="break-words text-lg font-semibold text-gray-900">
                                        {item.value}
                                    </p>
                                </div>
                            ))}

                        </div>

                    </div>

                </div>

                {/* ================================================== */}
                {/* Account Status */}
                {/* ================================================== */}

                <div className="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm">

                    <div className="space-y-5">

                        <div>
                            <h2 className="text-xl font-semibold text-gray-900">
                                Account Status
                            </h2>

                            <p className="mt-1 text-sm text-gray-500">
                                Current status of your CommuteShare account.
                            </p>
                        </div>

                        <div className="grid gap-4 sm:grid-cols-2">

                            <div className="flex items-center gap-4 rounded-xl border border-gray-200 p-5">

                                <div className="flex h-11 w-11 items-center justify-center rounded-full bg-green-100">
                                    <BadgeCheck
                                        size={22}
                                        className="text-green-600"
                                    />
                                </div>

                                <div>
                                    <p className="font-semibold text-gray-900">
                                        Account Status
                                    </p>

                                    <p className="text-sm text-gray-500">
                                        {user.is_active
                                            ? "Your account is active."
                                            : "Your account is inactive."}
                                    </p>
                                </div>

                            </div>

                            <div className="flex items-center gap-4 rounded-xl border border-gray-200 p-5">

                                <div className="flex h-11 w-11 items-center justify-center rounded-full bg-blue-100">
                                    <Shield
                                        size={22}
                                        className="text-blue-600"
                                    />
                                </div>

                                <div>
                                    <p className="font-semibold text-gray-900">
                                        Verification
                                    </p>

                                    <p className="text-sm text-gray-500">
                                        {user.is_verified
                                            ? "Your account is verified."
                                            : "Your account is not verified yet."}
                                    </p>
                                </div>

                            </div>

                        </div>

                    </div>

                </div>

            </div>
        </Layout>
    );
}
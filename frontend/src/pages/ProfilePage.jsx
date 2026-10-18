import { useState } from "react";
import toast from "react-hot-toast";
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
import UserAvatar from "../components/common/UserAvatar";
import useAuth from "../hooks/useAuth";
import { updateProfile, uploadAvatar } from "../api/users";

export default function ProfilePage() {
    const { user, refreshUser } = useAuth();
    const [uploading, setUploading] = useState(false);
    const [editing, setEditing] = useState(false);
    const [savingProfile, setSavingProfile] = useState(false);
    const [profileForm, setProfileForm] = useState({ full_name: "", phone_number: "", bio: "" });

    function startProfileEdit() {
        setProfileForm({ full_name: user.full_name ?? "", phone_number: user.phone_number ?? "", bio: user.bio ?? "" });
        setEditing(true);
    }

    async function saveProfile(event) {
        event.preventDefault();
        setSavingProfile(true);
        try {
            await updateProfile(profileForm);
            await refreshUser();
            setEditing(false);
            toast.success("Profile updated.");
        } catch (error) {
            toast.error(error.response?.data?.detail || "Could not update profile.");
        } finally {
            setSavingProfile(false);
        }
    }

    async function handleAvatarUpload(event) {
        const file = event.target.files?.[0];
        event.target.value = "";
        if (!file) return;
        if (!new Set(["image/jpeg", "image/png", "image/webp"]).has(file.type)) {
            toast.error("Choose a JPEG, PNG, or WebP image.");
            return;
        }
        if (file.size > 5 * 1024 * 1024) {
            toast.error("Avatar images must be 5 MB or smaller.");
            return;
        }
        setUploading(true);
        try {
            await uploadAvatar(file);
            await refreshUser();
            toast.success("Profile photo updated.");
        } catch (error) {
            toast.error(error.response?.data?.detail || "Could not upload profile photo.");
        } finally {
            setUploading(false);
        }
    }

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

                        <div className="flex shrink-0 flex-col items-center gap-3">
                            <div className="h-24 w-24 overflow-hidden rounded-full border-4 border-white/30 bg-white shadow-lg">
                                <UserAvatar user={user} alt={`${user.full_name}'s avatar`} className="h-full w-full object-cover" />
                            </div>
                            <label
                                htmlFor="avatar-upload"
                                aria-busy={uploading}
                                className={`inline-flex min-h-11 cursor-pointer items-center justify-center rounded-lg bg-white px-4 py-2 text-sm font-semibold text-blue-700 shadow-sm transition hover:bg-blue-50 focus-within:outline focus-within:outline-2 focus-within:outline-offset-2 focus-within:outline-white ${uploading ? "cursor-wait opacity-70" : ""}`}
                            >
                                {uploading ? "Uploading…" : "Upload photo"}
                                <input
                                    id="avatar-upload"
                                    className="sr-only"
                                    type="file"
                                    accept="image/jpeg,image/png,image/webp"
                                    disabled={uploading}
                                    onChange={handleAvatarUpload}
                                    aria-label="Upload profile photo"
                                />
                            </label>
                            <p className="text-center text-xs text-blue-100">Optional · JPEG, PNG, or WebP · up to 5 MB</p>
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
                        {editing ? (
                            <form onSubmit={saveProfile} className="space-y-4">
                                <label className="block text-sm font-medium text-gray-700" htmlFor="profile-full-name">Full name
                                    <input id="profile-full-name" required minLength={2} maxLength={100} value={profileForm.full_name} onChange={(event) => setProfileForm((current) => ({ ...current, full_name: event.target.value }))} className="mt-1 w-full rounded-xl border border-gray-300 px-4 py-3" />
                                </label>
                                <label className="block text-sm font-medium text-gray-700" htmlFor="profile-phone">Phone number
                                    <input id="profile-phone" type="tel" maxLength={20} autoComplete="tel" value={profileForm.phone_number} onChange={(event) => setProfileForm((current) => ({ ...current, phone_number: event.target.value }))} className="mt-1 w-full rounded-xl border border-gray-300 px-4 py-3" />
                                </label>
                                <label className="block text-sm font-medium text-gray-700" htmlFor="profile-bio">Bio
                                    <textarea id="profile-bio" maxLength={500} rows={3} value={profileForm.bio} onChange={(event) => setProfileForm((current) => ({ ...current, bio: event.target.value }))} className="mt-1 w-full rounded-xl border border-gray-300 px-4 py-3" />
                                </label>
                                <div className="flex flex-wrap gap-3">
                                    <button disabled={savingProfile} type="submit" className="min-h-11 rounded-xl bg-blue-600 px-5 py-2 font-medium text-white disabled:opacity-60">{savingProfile ? "Saving…" : "Save profile"}</button>
                                    <button disabled={savingProfile} type="button" onClick={() => setEditing(false)} className="min-h-11 rounded-xl border border-gray-300 px-5 py-2 font-medium text-gray-700">Cancel</button>
                                </div>
                            </form>
                        ) : (
                            <>
                                <div className="grid gap-5 md:grid-cols-2">
                                    {profileItems.map((item) => (
                                        <div key={item.label} className="rounded-xl border border-gray-200 p-5 transition hover:border-blue-400 hover:shadow-md">
                                            <div className="mb-2 flex items-center gap-2">{item.icon}<span className="text-sm font-medium text-gray-500">{item.label}</span></div>
                                            <p className="break-words text-lg font-semibold text-gray-900">{item.value}</p>
                                        </div>
                                    ))}
                                </div>
                                <button type="button" onClick={startProfileEdit} className="min-h-11 rounded-xl bg-blue-600 px-5 py-2 font-medium text-white">Edit profile</button>
                            </>
                        )}

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

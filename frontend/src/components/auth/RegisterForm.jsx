import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import toast from "react-hot-toast";

import useAuth from "../../hooks/useAuth";

export default function RegisterForm() {
    const navigate = useNavigate();

    const { register } = useAuth();

    const [form, setForm] = useState({
        full_name: "",
        email: "",
        phone_number: "",
        bio: "",
        profile_image: "",
        role: "PASSENGER",
        password: "",
        confirmPassword: "",
    });

    const [loading, setLoading] = useState(false);

    function handleChange(e) {
        setForm((prev) => ({
            ...prev,
            [e.target.name]: e.target.value,
        }));
    }

    async function handleSubmit(e) {
        e.preventDefault();

        if (form.password !== form.confirmPassword) {
            toast.error("Passwords do not match.");
            return;
        }

        const payload = {
            full_name: form.full_name,
            email: form.email,
            phone_number: form.phone_number,
            bio: form.bio,
            profile_image: form.profile_image,
            role: form.role,
            password: form.password,
        };

        try {
            setLoading(true);

            await register(payload);

            toast.success("Registration successful!");

            navigate("/login");
        } catch (error) {
            toast.error(
                error.response?.data?.detail ??
                    "Registration failed."
            );
        } finally {
            setLoading(false);
        }
    }

    return (
        <div className="max-w-md mx-auto">
            <div className="bg-white rounded-2xl shadow-lg p-8">
                <h1 className="text-3xl font-bold text-center text-gray-800">
                    Create Account
                </h1>

                <p className="text-center text-gray-500 mt-2 mb-8">
                    Join CommuteShare today.
                </p>

                <form
                    onSubmit={handleSubmit}
                    className="space-y-5"
                >
                    <div>
                        <label className="block mb-2 text-sm font-medium text-gray-700">
                            Full Name
                        </label>

                        <input
                            className="w-full rounded-lg border border-gray-300 p-3 focus:outline-none focus:ring-2 focus:ring-green-500"
                            name="full_name"
                            placeholder="Enter your full name"
                            value={form.full_name}
                            onChange={handleChange}
                            required
                        />
                    </div>

                    <div>
                        <label className="block mb-2 text-sm font-medium text-gray-700">
                            Email
                        </label>

                        <input
                            className="w-full rounded-lg border border-gray-300 p-3 focus:outline-none focus:ring-2 focus:ring-green-500"
                            type="email"
                            name="email"
                            placeholder="Enter your email"
                            value={form.email}
                            onChange={handleChange}
                            required
                        />
                    </div>

                    <div>
                        <label className="block mb-2 text-sm font-medium text-gray-700">
                            Phone Number
                        </label>

                        <input
                            className="w-full rounded-lg border border-gray-300 p-3 focus:outline-none focus:ring-2 focus:ring-green-500"
                            name="phone_number"
                            placeholder="Optional"
                            value={form.phone_number}
                            onChange={handleChange}
                        />
                    </div>

                    <div>
                        <label className="block mb-2 text-sm font-medium text-gray-700">
                            Bio
                        </label>

                        <textarea
                            className="w-full rounded-lg border border-gray-300 p-3 focus:outline-none focus:ring-2 focus:ring-green-500"
                            rows="3"
                            name="bio"
                            placeholder="Tell us something about yourself"
                            value={form.bio}
                            onChange={handleChange}
                        />
                    </div>

                    <div>
                        <label className="block mb-2 text-sm font-medium text-gray-700">
                            Profile Image URL
                        </label>

                        <input
                            className="w-full rounded-lg border border-gray-300 p-3 focus:outline-none focus:ring-2 focus:ring-green-500"
                            name="profile_image"
                            placeholder="Optional"
                            value={form.profile_image}
                            onChange={handleChange}
                        />
                    </div>

                    <div>
                        <label className="block mb-2 text-sm font-medium text-gray-700">
                            Role
                        </label>

                        <select
                            name="role"
                            value={form.role}
                            onChange={handleChange}
                            className="w-full rounded-lg border border-gray-300 p-3 focus:outline-none focus:ring-2 focus:ring-green-500"
                        >
                            <option value="PASSENGER">
                                Passenger
                            </option>

                            <option value="DRIVER">
                                Driver
                            </option>
                        </select>
                    </div>

                    <div>
                        <label className="block mb-2 text-sm font-medium text-gray-700">
                            Password
                        </label>

                        <input
                            className="w-full rounded-lg border border-gray-300 p-3 focus:outline-none focus:ring-2 focus:ring-green-500"
                            type="password"
                            name="password"
                            placeholder="Minimum 8 characters"
                            value={form.password}
                            onChange={handleChange}
                            required
                        />
                    </div>

                    <div>
                        <label className="block mb-2 text-sm font-medium text-gray-700">
                            Confirm Password
                        </label>

                        <input
                            className="w-full rounded-lg border border-gray-300 p-3 focus:outline-none focus:ring-2 focus:ring-green-500"
                            type="password"
                            name="confirmPassword"
                            placeholder="Re-enter your password"
                            value={form.confirmPassword}
                            onChange={handleChange}
                            required
                        />
                    </div>

                    <button
                        type="submit"
                        disabled={loading}
                        className="w-full rounded-lg bg-green-600 p-3 font-semibold text-white transition hover:bg-green-700 disabled:cursor-not-allowed disabled:bg-green-400"
                    >
                        {loading
                            ? "Creating Account..."
                            : "Register"}
                    </button>
                </form>

                <p className="mt-6 text-center text-sm text-gray-600">
                    Already have an account?{" "}
                    <Link
                        to="/login"
                        className="font-semibold text-green-600 hover:text-green-700"
                    >
                        Login →
                    </Link>
                </p>
            </div>
        </div>
    );
}
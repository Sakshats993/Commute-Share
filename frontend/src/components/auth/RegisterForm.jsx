import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Eye, EyeOff } from "lucide-react";
import toast from "react-hot-toast";

import useAuth from "../../hooks/useAuth";
import { normalizeIndianMobileNumber } from "../../utils/phone";
import { passwordsMatch } from "../../utils/passwordConfirmation";
import UserAvatar from "../common/UserAvatar";
import OAuthButtons from "./OAuthButtons";

export default function RegisterForm() {
    const navigate = useNavigate();

    const { register } = useAuth();

    const [form, setForm] = useState({
        full_name: "",
        email: "",
        phone_number: "",
        role: "passenger",
        password: "",
        confirmPassword: "",
    });

    const [loading, setLoading] = useState(false);
    const [submitError, setSubmitError] = useState("");
    const [showPassword, setShowPassword] = useState(false);
    const [showConfirmPassword, setShowConfirmPassword] = useState(false);

    function handleChange(e) {
        setSubmitError("");
        setForm((prev) => ({
            ...prev,
            [e.target.name]: e.target.value,
        }));
    }

    async function handleSubmit(e) {
        e.preventDefault();
        if (loading) return;

        if (!passwordsMatch(form.password, form.confirmPassword)) {
            setSubmitError("Passwords do not match.");
            return;
        }

        const phoneNumber = normalizeIndianMobileNumber(form.phone_number);
        if (!phoneNumber) {
            setSubmitError("Enter a valid 10-digit Indian mobile number, with or without the +91 country code.");
            return;
        }

        const payload = {
            full_name: form.full_name,
            email: form.email,
            phone_number: phoneNumber,
            role: form.role,
            password: form.password,
        };

        try {
            setLoading(true);

            await register(payload);

            toast.success("Registration successful!");

            navigate("/login");
        } catch (error) {
            const detail = error.response?.data?.detail;

            const message = Array.isArray(detail)
                ? detail.map((item) => item.msg).join(", ")
                : detail || "Registration failed. Please try again.";
            setSubmitError(message);
        } finally {
            setLoading(false);
        }
    }

    return (
        <>
            <div className="mb-6 text-center">
                <h1 className="text-2xl font-bold tracking-tight text-center text-gray-900 sm:text-[1.75rem]">
                    Create account
                </h1>

                <p className="mt-2 text-center text-gray-600">
                    Join CommuteShare today.
                </p>
            </div>

            <OAuthButtons action="sign up" />

            <p className="my-5 text-center text-sm text-gray-500">Or create an account with email</p>

            <form onSubmit={handleSubmit} className="space-y-5">
                <div>
                    <label htmlFor="register-name" className="block mb-2 text-sm font-medium text-gray-700">
                        Full name
                    </label>

                    <input
                        id="register-name"
                        className="w-full rounded-lg border border-gray-300 p-3 focus:outline-none focus:ring-2 focus:ring-green-500"
                        name="full_name"
                        placeholder="Enter your full name"
                        value={form.full_name}
                        onChange={handleChange}
                        required
                        minLength={2}
                        maxLength={100}
                        autoComplete="name"
                        autoCapitalize="words"
                        autoCorrect="off"
                    />
                </div>

                <div>
                    <label htmlFor="register-email" className="block mb-2 text-sm font-medium text-gray-700">
                        Email
                    </label>

                    <input
                        id="register-email"
                        className="w-full rounded-lg border border-gray-300 p-3 focus:outline-none focus:ring-2 focus:ring-green-500"
                        type="email"
                        name="email"
                        placeholder="Enter your email"
                        value={form.email}
                        onChange={handleChange}
                        required
                        autoComplete="email"
                        autoCapitalize="none"
                        autoCorrect="off"
                        spellCheck={false}
                        inputMode="email"
                    />
                </div>

                <div>
                    <label htmlFor="register-phone" className="block mb-2 text-sm font-medium text-gray-700">
                        Phone number
                    </label>

                    <input
                        id="register-phone"
                        type="tel"
                        className="w-full rounded-lg border border-gray-300 p-3 focus:outline-none focus:ring-2 focus:ring-green-500"
                        name="phone_number"
                        placeholder="Enter your phone number"
                        value={form.phone_number}
                        maxLength={16}
                        pattern={"(?:\\+?91(?: |-)?)?[6-9][0-9]{4}(?: |-)?[0-9]{5}"}
                        title="Enter a valid 10-digit Indian mobile number. You may include the 91 country code."
                        inputMode="tel"
                        autoComplete="tel"
                        aria-describedby="register-phone-help"
                        onChange={handleChange}
                        required
                    />
                    <p id="register-phone-help" className="mt-1.5 text-xs text-gray-500">
                        Required for email registration. Enter 10 digits; +91 is optional. We don’t send verification codes.
                    </p>
                </div>

                <fieldset>
                    <legend className="mb-2 text-sm font-medium text-gray-700">Choose your role</legend>
                    <div className="grid grid-cols-2 gap-3">
                        {[
                            { value: "passenger", label: "Passenger", description: "Book rides" },
                            { value: "driver", label: "Driver", description: "Offer rides" },
                        ].map((option) => {
                            const selected = form.role === option.value;
                            return (
                                <label
                                    key={option.value}
                                    className={`flex min-h-28 cursor-pointer flex-col items-center justify-center gap-2 rounded-xl border p-3 text-center transition focus-within:outline focus-within:outline-2 focus-within:outline-offset-2 focus-within:outline-green-600 ${
                                        selected
                                            ? "border-green-600 bg-green-50 ring-1 ring-green-600 dark:bg-green-950"
                                            : "border-gray-300 hover:bg-gray-50 dark:hover:bg-slate-700"
                                    }`}
                                >
                                    <input
                                        className="sr-only"
                                        type="radio"
                                        name="role"
                                        value={option.value}
                                        checked={selected}
                                        onChange={handleChange}
                                    />
                                    <UserAvatar user={{ role: option.value }} alt="" className="h-12 w-12 rounded-full" />
                                    <span className="text-sm font-semibold text-gray-800">{option.label}</span>
                                    <span className="text-xs text-gray-600">{option.description}</span>
                                </label>
                            );
                        })}
                    </div>
                    <p className="mt-2 text-xs text-gray-500">
                        This avatar is used by default. You can upload a photo later from your profile.
                    </p>
                </fieldset>

                <div>
                    <label htmlFor="register-password" className="block mb-2 text-sm font-medium text-gray-700">
                        Password
                    </label>

                    <div className="relative">
                        <input
                            id="register-password"
                            className="w-full rounded-lg border border-gray-300 p-3 pr-12 focus:outline-none focus:ring-2 focus:ring-green-500"
                            type={showPassword ? "text" : "password"}
                            name="password"
                            placeholder="Minimum 8 characters"
                            value={form.password}
                            onChange={handleChange}
                            required
                            minLength={8}
                            maxLength={128}
                            autoComplete="new-password"
                            autoCapitalize="none"
                            spellCheck={false}
                        />
                        <button
                            type="button"
                            onClick={() => setShowPassword((visible) => !visible)}
                            aria-label={showPassword ? "Hide password" : "Show password"}
                            aria-pressed={showPassword}
                            className="absolute inset-y-0 right-0 flex w-11 items-center justify-center rounded-r-lg text-gray-600 hover:text-gray-900 focus-visible:outline-2 focus-visible:outline-green-600"
                        >
                            {showPassword ? <EyeOff size={19} aria-hidden="true" /> : <Eye size={19} aria-hidden="true" />}
                        </button>
                    </div>
                </div>

                <div>
                    <label htmlFor="register-confirm-password" className="block mb-2 text-sm font-medium text-gray-700">
                        Confirm password
                    </label>
                    <div className="relative">
                        <input
                            id="register-confirm-password"
                            className="w-full rounded-lg border border-gray-300 p-3 pr-12 focus:outline-none focus:ring-2 focus:ring-green-500"
                            type={showConfirmPassword ? "text" : "password"}
                            name="confirmPassword"
                            placeholder="Re-enter your password"
                            value={form.confirmPassword}
                            onChange={handleChange}
                            required
                            minLength={8}
                            maxLength={128}
                            autoComplete="new-password"
                            autoCapitalize="none"
                            spellCheck={false}
                            aria-invalid={Boolean(form.confirmPassword && !passwordsMatch(form.password, form.confirmPassword))}
                            aria-describedby={form.confirmPassword && !passwordsMatch(form.password, form.confirmPassword) ? "register-password-match-error" : undefined}
                        />
                        <button
                            type="button"
                            onClick={() => setShowConfirmPassword((visible) => !visible)}
                            aria-label={showConfirmPassword ? "Hide confirmation password" : "Show confirmation password"}
                            aria-pressed={showConfirmPassword}
                            className="absolute inset-y-0 right-0 flex w-11 items-center justify-center rounded-r-lg text-gray-600 hover:text-gray-900 focus-visible:outline-2 focus-visible:outline-green-600"
                        >
                            {showConfirmPassword ? <EyeOff size={19} aria-hidden="true" /> : <Eye size={19} aria-hidden="true" />}
                        </button>
                    </div>
                    {form.confirmPassword && !passwordsMatch(form.password, form.confirmPassword) && (
                        <p id="register-password-match-error" className="mt-1.5 text-xs text-red-700">Passwords do not match.</p>
                    )}
                </div>

                {submitError && (
                    <p role="alert" className="rounded-lg bg-red-50 px-4 py-3 text-sm text-red-700">
                        {submitError}
                    </p>
                )}

                <button
                    type="submit"
                    disabled={loading}
                    aria-busy={loading}
                    className="w-full rounded-lg bg-green-600 p-3 font-semibold text-white transition hover:bg-green-700 disabled:cursor-not-allowed disabled:bg-green-400"
                >
                    {loading
                        ? "Creating account…"
                        : "Create account"}
                </button>
            </form>

            <p className="mt-7 border-t border-slate-200 pt-5 text-center text-sm text-gray-600">
                Already have an account?{" "}
                <Link
                    to="/login"
                    className="font-semibold text-green-600 hover:text-green-700"
                >
                    Sign in →
                </Link>
            </p>
        </>
    );
}

import { useState } from "react";
import { Link } from "react-router-dom";

import { requestPasswordReset } from "../api/auth";
import { getApiErrorMessage } from "../utils/apiError";
import ThemeToggle from "../components/common/ThemeToggle";

export default function ForgotPasswordPage() {
    const [email, setEmail] = useState("");
    const [loading, setLoading] = useState(false);
    const [message, setMessage] = useState("");
    const [error, setError] = useState("");

    async function handleSubmit(event) {
        event.preventDefault();
        setLoading(true);
        setError("");
        setMessage("");
        try {
            const response = await requestPasswordReset(email);
            setMessage(response.message);
        } catch (requestError) {
            const fallback = requestError.response?.status === 503
                ? "Password reset email is not configured on this server yet."
                : "We couldn't submit the request. Please try again.";
            setError(getApiErrorMessage(requestError, fallback));
        } finally {
            setLoading(false);
        }
    }

    return (
        <main className="login-page flex min-h-screen items-center justify-center bg-slate-100 px-4 py-10">
            <ThemeToggle />
            <section className="w-full max-w-md rounded-2xl bg-white p-5 shadow-lg sm:p-8">
                <h1 className="text-center text-3xl font-bold text-gray-800">Forgot password?</h1>
                <p className="mb-7 mt-2 text-center text-gray-600">
                    Enter the email address on your account. If it matches an active account, we’ll send a reset link.
                </p>
                <form onSubmit={handleSubmit} className="space-y-5">
                    <div>
                        <label htmlFor="reset-request-email" className="mb-2 block text-sm font-medium text-gray-700">Email</label>
                        <input
                            id="reset-request-email"
                            type="email"
                            autoComplete="email"
                            autoCapitalize="none"
                            required
                            value={email}
                            onChange={(event) => setEmail(event.target.value)}
                            className="w-full rounded-lg border border-gray-300 p-3 focus:outline-none focus:ring-2 focus:ring-green-500"
                            placeholder="Enter your account email"
                        />
                    </div>
                    {message && <p role="status" className="rounded-lg bg-green-50 px-4 py-3 text-sm text-green-800">{message}</p>}
                    {error && <p role="alert" className="rounded-lg bg-red-50 px-4 py-3 text-sm text-red-700">{error}</p>}
                    <button
                        type="submit"
                        disabled={loading}
                        aria-busy={loading}
                        className="w-full rounded-lg bg-green-600 p-3 font-semibold text-white hover:bg-green-700 disabled:cursor-not-allowed disabled:opacity-60"
                    >
                        {loading ? "Sending…" : "Send reset link"}
                    </button>
                </form>
                <p className="mt-6 text-center text-sm">
                    <Link to="/login" className="font-semibold text-green-700 hover:underline">Back to login</Link>
                </p>
            </section>
        </main>
    );
}

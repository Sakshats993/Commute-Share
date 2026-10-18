import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import { confirmPasswordReset } from "../api/auth";
import { getApiErrorMessage } from "../utils/apiError";
import ThemeToggle from "../components/common/ThemeToggle";

export default function ResetPasswordPage() {
    const [token] = useState(() => {
        const params = new URLSearchParams(window.location.hash.slice(1));
        return params.get("token") || "";
    });
    const [password, setPassword] = useState("");
    const [confirmation, setConfirmation] = useState("");
    const [loading, setLoading] = useState(false);
    const [success, setSuccess] = useState(false);
    const [error, setError] = useState("");

    useEffect(() => {
        if (window.location.hash) {
            window.history.replaceState({}, document.title, window.location.pathname);
        }
    }, []);

    async function handleSubmit(event) {
        event.preventDefault();
        setError("");
        if (password !== confirmation) {
            setError("Passwords do not match.");
            return;
        }

        setLoading(true);
        try {
            await confirmPasswordReset(token, password);
            setSuccess(true);
        } catch (requestError) {
            setError(getApiErrorMessage(requestError, "This reset link is invalid or expired. Request a new link."));
        } finally {
            setLoading(false);
        }
    }

    return (
        <main className="login-page flex min-h-screen items-center justify-center bg-slate-100 px-4 py-10">
            <ThemeToggle />
            <section className="w-full max-w-md rounded-2xl bg-white p-5 shadow-lg sm:p-8">
                {success ? (
                    <div className="text-center">
                        <h1 className="text-2xl font-bold text-gray-800">Password updated</h1>
                        <p className="mt-3 text-gray-600">You can now sign in with your new password.</p>
                        <Link to="/login" className="mt-5 inline-block font-semibold text-green-700 hover:underline">Go to login</Link>
                    </div>
                ) : (
                    <>
                        <h1 className="text-center text-3xl font-bold text-gray-800">Choose a new password</h1>
                        <p className="mb-7 mt-2 text-center text-gray-600">Use at least 8 characters.</p>
                        {token ? (
                            <form onSubmit={handleSubmit} className="space-y-5">
                                <div>
                                    <label htmlFor="new-password" className="mb-2 block text-sm font-medium text-gray-700">New password</label>
                                    <input id="new-password" type="password" autoComplete="new-password" required minLength={8} maxLength={128} value={password} onChange={(event) => setPassword(event.target.value)} className="w-full rounded-lg border border-gray-300 p-3 focus:outline-none focus:ring-2 focus:ring-green-500" />
                                </div>
                                <div>
                                    <label htmlFor="confirm-new-password" className="mb-2 block text-sm font-medium text-gray-700">Confirm new password</label>
                                    <input id="confirm-new-password" type="password" autoComplete="new-password" required minLength={8} maxLength={128} value={confirmation} onChange={(event) => setConfirmation(event.target.value)} className="w-full rounded-lg border border-gray-300 p-3 focus:outline-none focus:ring-2 focus:ring-green-500" />
                                </div>
                                {error && <p role="alert" className="rounded-lg bg-red-50 px-4 py-3 text-sm text-red-700">{error}</p>}
                                <button type="submit" disabled={loading} aria-busy={loading} className="w-full rounded-lg bg-green-600 p-3 font-semibold text-white hover:bg-green-700 disabled:cursor-not-allowed disabled:opacity-60">
                                    {loading ? "Updating…" : "Update password"}
                                </button>
                            </form>
                        ) : (
                            <p role="alert" className="rounded-lg bg-red-50 px-4 py-3 text-center text-sm text-red-700">
                                This reset link is invalid or expired. <Link to="/forgot-password" className="font-semibold underline">Request a new one</Link>.
                            </p>
                        )}
                    </>
                )}
            </section>
        </main>
    );
}

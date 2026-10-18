import { useEffect, useRef, useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import useAuth from "../hooks/useAuth";
import ThemeToggle from "../components/common/ThemeToggle";

export default function OAuthCallbackPage() {
    const navigate = useNavigate();
    const { loginWithAccessToken } = useAuth();
    const processed = useRef(false);
    const [error, setError] = useState("");

    useEffect(() => {
        if (processed.current) return;
        processed.current = true;

        const params = new URLSearchParams(window.location.hash.slice(1));
        const token = params.get("access_token");
        window.history.replaceState({}, document.title, window.location.pathname);

        if (!token) {
            setError("The sign-in response was incomplete. Please try again.");
            return;
        }

        loginWithAccessToken(token)
            .then(() => navigate("/dashboard", { replace: true }))
            .catch(() => setError("CommuteShare could not complete sign-in. Please try again."));
    }, [loginWithAccessToken, navigate]);

    return (
        <main className="login-page flex min-h-screen items-center justify-center bg-slate-100 px-4 py-10">
            <ThemeToggle />
            <section className="w-full max-w-md rounded-2xl bg-white p-8 text-center shadow-lg" aria-live="polite">
                {error ? (
                    <>
                        <h1 className="text-2xl font-bold text-gray-800">Sign-in failed</h1>
                        <p className="mt-3 text-gray-600">{error}</p>
                        <Link className="mt-5 inline-block font-semibold text-green-700 hover:underline" to="/login">
                            Return to login
                        </Link>
                    </>
                ) : (
                    <p className="text-gray-700">Completing sign-in…</p>
                )}
            </section>
        </main>
    );
}

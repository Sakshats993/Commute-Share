import { useEffect, useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { Eye, EyeOff } from "lucide-react";
import toast from "react-hot-toast";

import useAuth from "../../hooks/useAuth";
import { getApiErrorMessage } from "../../utils/apiError";
import OAuthButtons from "./OAuthButtons";

export default function LoginForm() {
    const navigate = useNavigate();
    const location = useLocation();
    const { login } = useAuth();

    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [showPassword, setShowPassword] = useState(false);
    const [loading, setLoading] = useState(false);
    const [submitError, setSubmitError] = useState("");

    useEffect(() => {
        const reason = new URLSearchParams(location.search).get("oauth_error");
        if (reason) {
            const messages = {
                not_configured: "Social sign-in is not configured yet. Use email and password or contact the site administrator.",
                insecure_config: "Social sign-in requires HTTPS outside local development. Contact the site administrator.",
                account_required: "We couldn't create your account. Please try email registration or contact support.",
                account_unavailable: "This account cannot sign in with that provider. Use email and password or contact support.",
                invalid_state: "Sign-in could not be verified. Please try again.",
                cancelled: "Social sign-in was cancelled.",
                provider_error: "The provider could not complete sign-in. Please try again.",
            };
            setSubmitError(messages[reason] || "Social sign-in failed. Please try again.");
            navigate("/login", { replace: true });
        }

    }, [location.search, navigate]);

    async function handleSubmit(e) {
        e.preventDefault();
        if (loading) return;
        setSubmitError("");

        try {
            setLoading(true);

            await login(email, password);

            toast.success("Login successful!");

            navigate("/dashboard");
        } catch (error) {
            const message = getApiErrorMessage(error, "Invalid email or password.");
            setSubmitError(message);
        } finally {
            setLoading(false);
        }
    }

    return (
        <>
            <div className="mb-7 text-center">
                <h1 className="text-2xl font-bold tracking-tight text-gray-900 sm:text-[1.75rem]">
                    Welcome back
                </h1>

                <p className="mt-2 text-gray-500">
                    Sign in to continue using CommuteShare.
                </p>
            </div>

            <OAuthButtons />
            <p className="my-5 text-center text-sm text-gray-500">Or sign in with email</p>

            <form onSubmit={handleSubmit} className="space-y-5">
                <div>
                    <label htmlFor="login-email" className="block mb-2 text-sm font-medium text-gray-700">
                        Email
                    </label>

                    <input
                        id="login-email"
                        type="email"
                        name="email"
                        autoComplete="email"
                        autoCapitalize="none"
                        autoCorrect="off"
                        spellCheck={false}
                        inputMode="email"
                        placeholder="Enter your email"
                        className="w-full rounded-lg border border-gray-300 p-3 focus:outline-none focus:ring-2 focus:ring-green-500"
                        value={email}
                        onChange={(e) => {
                            setEmail(e.target.value);
                            setSubmitError("");
                        }}
                        required
                    />
                </div>

                <div>
                    <div className="mb-2 flex items-center justify-between gap-3">
                        <label htmlFor="login-password" className="text-sm font-medium text-gray-700">
                            Password
                        </label>
                        <Link to="/forgot-password" className="text-sm font-semibold text-green-700 hover:underline">
                            Forgot password?
                        </Link>
                    </div>

                    <div className="relative">
                        <input
                            id="login-password"
                            type={showPassword ? "text" : "password"}
                            name="password"
                            autoComplete="current-password"
                            autoCapitalize="none"
                            spellCheck={false}
                            placeholder="Enter your password"
                            className="w-full rounded-lg border border-gray-300 p-3 pr-12 focus:outline-none focus:ring-2 focus:ring-green-500"
                            value={password}
                            onChange={(e) => {
                                setPassword(e.target.value);
                                setSubmitError("");
                            }}
                            required
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
                    {loading ? "Signing in…" : "Sign in"}
                </button>
            </form>

            <div className="mt-7 border-t border-slate-200 pt-5 text-center">
                <p className="text-sm text-gray-600">
                    Don’t have an account?
                </p>

                <Link
                    to="/register"
                    className="mt-2 inline-block font-semibold text-green-600 transition hover:text-green-700 hover:underline"
                >
                    Create account →
                </Link>
            </div>
        </>
    );
}

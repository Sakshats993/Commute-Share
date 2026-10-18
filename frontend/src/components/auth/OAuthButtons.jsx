import { useEffect, useState } from "react";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://127.0.0.1:8000";

function ProviderLogo({ provider }) {
    if (provider === "google") {
        return (
            <svg aria-hidden="true" viewBox="0 0 24 24" className="h-5 w-5 shrink-0">
                <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.09-1.92 3.28-4.75 3.28-8.09z" />
                <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.99.66-2.25 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.15v2.84C3.96 20.53 7.7 23 12 23z" />
                <path fill="#FBBC05" d="M5.84 14.1c-.22-.66-.35-1.36-.35-2.1s.13-1.44.35-2.1V7.06H2.15C1.42 8.48 1 10.18 1 12s.42 3.52 1.15 4.94l3.69-2.84z" />
                <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.96 3.47 2.15 7.06l3.69 2.84C6.71 7.31 9.14 5.38 12 5.38z" />
            </svg>
        );
    }

    return (
        <svg aria-hidden="true" viewBox="0 0 24 24" className="h-5 w-5 shrink-0 fill-current">
            <path d="M12 .5a12 12 0 0 0-3.79 23.39c.6.11.82-.26.82-.58v-2.23c-3.34.73-4.04-1.42-4.04-1.42-.55-1.39-1.33-1.76-1.33-1.76-1.09-.75.08-.74.08-.74 1.2.08 1.84 1.23 1.84 1.23 1.07 1.84 2.8 1.31 3.49 1 .11-.78.42-1.31.76-1.61-2.67-.3-5.47-1.33-5.47-5.93 0-1.31.47-2.38 1.23-3.22-.12-.3-.53-1.52.12-3.17 0 0 1-.32 3.3 1.23a11.48 11.48 0 0 1 6 0c2.3-1.55 3.3-1.23 3.3-1.23.65 1.65.24 2.87.12 3.17.77.84 1.23 1.91 1.23 3.22 0 4.61-2.8 5.63-5.48 5.92.43.37.81 1.1.81 2.22v3.3c0 .32.22.69.82.57A12 12 0 0 0 12 .5z" />
        </svg>
    );
}

export default function OAuthButtons({ action = "sign in" }) {
    const [providers, setProviders] = useState({ google: false, github: false });

    useEffect(() => {
        let active = true;
        fetch(`${API_BASE_URL}/auth/providers`)
            .then((response) => (response.ok ? response.json() : null))
            .then((configured) => {
                if (active && configured) setProviders(configured);
            })
            .catch(() => {});

        return () => { active = false; };
    }, []);

    return (
        <div className="mt-6">
            <p className="mb-3 text-center text-sm font-medium text-gray-600">
                {action === "sign up" ? "Create an account with" : "Continue with"}
            </p>
            <div className="grid grid-cols-2 gap-3">
                {["google", "github"].map((provider) => {
                    const label = provider === "google" ? "Google" : "GitHub";
                    const configured = providers[provider];
                    return (
                        <button
                            key={provider}
                            type="button"
                            disabled={!configured}
                            onClick={() => window.location.assign(`${API_BASE_URL}/auth/oauth/${provider}/start`)}
                            aria-label={`Continue ${action} with ${label}`}
                            title={configured ? `Continue with ${label}` : `${label} sign-in needs backend OAuth credentials`}
                            className="flex min-h-11 items-center justify-center gap-2 rounded-lg border border-gray-300 px-3 py-2 text-sm font-semibold text-gray-700 transition hover:bg-gray-50 focus-visible:outline focus-visible:outline-2 focus-visible:outline-green-600 disabled:cursor-not-allowed disabled:opacity-60"
                        >
                            <ProviderLogo provider={provider} />
                            <span>{label}</span>
                        </button>
                    );
                })}
            </div>
            <p className="mt-3 text-center text-xs text-gray-500">
                {action === "sign up"
                    ? "We’ll use your verified email and available profile details. You can add a mobile number later."
                    : "New here? Your first sign-in creates an account from your verified email and available profile details."}
            </p>
        </div>
    );
}

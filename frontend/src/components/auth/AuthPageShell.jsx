import ThemeToggle from "../common/ThemeToggle";
import AuthBrand from "./AuthBrand";

export default function AuthPageShell({ children, className = "", showTopBrand = false }) {
    return (
        <main className={`auth-shell relative min-h-screen overflow-x-hidden ${showTopBrand ? "flex flex-col px-4 sm:px-6" : "flex items-center justify-center px-4 py-12 sm:px-6"}`}>
            {showTopBrand && (
                <header className="relative z-10 flex items-center pt-4 pr-12 sm:pt-6">
                    <AuthBrand variant="horizontal" />
                </header>
            )}
            <ThemeToggle />
            <div className={showTopBrand ? "flex flex-1 items-center justify-center py-8" : "flex w-full items-center justify-center"}>
                <section className={`auth-card relative z-0 w-full rounded-3xl border border-slate-200 bg-white p-6 shadow-xl shadow-slate-900/10 sm:p-9 ${className}`}>
                    {children}
                </section>
            </div>
        </main>
    );
}

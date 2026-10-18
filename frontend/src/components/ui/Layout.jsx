import { useState } from "react";
import Navbar from "../layout/Navbar";
import Sidebar from "../layout/Sidebar";

export default function Layout({
    children,
}) {
    const [mobileNavigationOpen, setMobileNavigationOpen] = useState(false);

    return (
        <div className="flex min-h-screen bg-slate-100">
            <a
                href="#main-content"
                className="sr-only fixed left-4 top-4 z-[100] rounded-lg bg-white px-4 py-3 text-slate-900 shadow focus:not-sr-only"
            >
                Skip to main content
            </a>
            {mobileNavigationOpen && (
                <button
                    type="button"
                    onClick={() => setMobileNavigationOpen(false)}
                    className="fixed inset-0 z-40 bg-slate-950/50 lg:hidden"
                    aria-label="Close navigation overlay"
                />
            )}
            <Sidebar
                mobileOpen={mobileNavigationOpen}
                onClose={() => setMobileNavigationOpen(false)}
            />

            <div className="flex min-w-0 flex-1 flex-col">
                <Navbar
                    mobileNavigationOpen={mobileNavigationOpen}
                    onMenuClick={() => setMobileNavigationOpen((open) => !open)}
                />

                <main id="main-content" tabIndex="-1" className="min-w-0 flex-1 overflow-auto p-4 sm:p-6 lg:p-8">
                    {children}
                </main>
            </div>
        </div>
    );
}

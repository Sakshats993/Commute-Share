import { useEffect, useRef, useState } from "react";
import {
    ChevronDown,
    LogOut,
    User,
    TriangleAlert,
    Menu,
    Moon,
    Sun,
} from "lucide-react";
import { Link, useNavigate } from "react-router-dom";

import useAuth from "../../hooks/useAuth";
import ROUTES from "../../constants/routes";
import UserAvatar from "../common/UserAvatar";
import AuthBrand from "../auth/AuthBrand";

export default function Navbar({
    onMenuClick = () => {},
    mobileNavigationOpen = false,
}) {
    const { user, logout } = useAuth();
    const navigate = useNavigate();

    const [open, setOpen] = useState(false);
    const [showLogoutModal, setShowLogoutModal] = useState(false);
    const [darkMode, setDarkMode] = useState(() => document.documentElement.classList.contains("dark"));

    function toggleTheme() {
        const next = !darkMode;
        document.documentElement.classList.toggle("dark", next);
        localStorage.setItem("commuteshare-theme", next ? "dark" : "light");
        setDarkMode(next);
    }

    const menuRef = useRef(null);

    useEffect(() => {
        function handleClickOutside(event) {
            if (menuRef.current && !menuRef.current.contains(event.target)) {
                setOpen(false);
            }
        }

        function handleEscape(event) {
            if (event.key === "Escape") {
                setShowLogoutModal(false);
                setOpen(false);
            }
        }

        document.addEventListener("mousedown", handleClickOutside);
        document.addEventListener("keydown", handleEscape);

        return () => {
            document.removeEventListener(
                "mousedown",
                handleClickOutside
            );
            document.removeEventListener(
                "keydown",
                handleEscape
            );
        };
    }, []);

    function confirmLogout() {
        logout();
        navigate(ROUTES.LOGIN);
    }

    function handleProfile() {
        setOpen(false);
        navigate(ROUTES.PROFILE);
    }

    return (
        <>
            <header className="sticky top-0 z-30 flex items-center justify-between border-b border-gray-200 bg-white px-4 py-3 shadow-sm sm:px-8 sm:py-4">
                <button
                    type="button"
                    onClick={onMenuClick}
                    className="rounded-lg p-2 text-slate-700 hover:bg-slate-100 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-600 lg:hidden"
                    aria-label={mobileNavigationOpen ? "Close navigation" : "Open navigation"}
                    aria-controls="primary-navigation"
                    aria-expanded={mobileNavigationOpen}
                >
                    <Menu size={22} aria-hidden="true" />
                </button>
                <Link to={ROUTES.DASHBOARD} aria-label="CommuteShare dashboard" className="ml-1 flex min-w-0 items-center lg:hidden">
                    <AuthBrand variant="navbar" />
                </Link>
                <button type="button" onClick={toggleTheme} aria-label={`Switch to ${darkMode ? "light" : "dark"} mode`} aria-pressed={darkMode} className="ml-auto mr-2 rounded-lg p-2 text-slate-700 transition hover:bg-slate-100 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-600">
                    {darkMode ? <Sun size={20} aria-hidden="true" /> : <Moon size={20} aria-hidden="true" />}
                </button>
                <div className="relative" ref={menuRef}>
                    <button
                        type="button"
                        onClick={() => setOpen((current) => !current)}
                        className="flex items-center gap-3 rounded-xl px-3 py-2 hover:bg-gray-100 transition-all duration-200"
                        aria-expanded={open}
                        aria-label={`Account menu for ${user?.full_name ?? "user"}`}
                        aria-controls="account-menu"
                    >
                        <UserAvatar user={user} className="h-10 w-10 rounded-full object-cover" />

                        <span className="hidden font-semibold text-gray-800 sm:inline">
                            {user?.full_name}
                        </span>

                        <ChevronDown
                            size={18}
                            className={`text-gray-600 transition-transform duration-200 ${
                                open ? "rotate-180" : ""
                            }`}
                        />
                    </button>

                    {open && (
                        <div id="account-menu" className="absolute right-0 mt-3 w-64 overflow-hidden rounded-2xl border border-gray-200 bg-white shadow-xl z-50">
                            <div className="border-b px-5 py-4">
                                <p className="font-semibold text-gray-900">
                                    {user?.full_name}
                                </p>

                                <p className="text-sm text-gray-500 truncate">
                                    {user?.email}
                                </p>
                            </div>

                            <button
                                type="button"
                                onClick={handleProfile}
                                className="flex w-full items-center gap-3 px-5 py-3 text-gray-700 hover:bg-gray-100 transition"
                            >
                                <User size={18} />
                                My Profile
                            </button>

                            <button
                                type="button"
                                onClick={() => {
                                    setOpen(false);
                                    setShowLogoutModal(true);
                                }}
                                className="flex w-full items-center gap-3 px-5 py-3 text-red-600 hover:bg-red-50 transition"
                            >
                                <LogOut size={18} />
                                Logout
                            </button>
                        </div>
                    )}
                </div>
            </header>

            {showLogoutModal && (
                <div className="fixed inset-0 z-[100] flex items-center justify-center bg-black/40 p-4 backdrop-blur-sm">
                    <div role="dialog" aria-modal="true" aria-labelledby="logout-title" className="w-[min(420px,calc(100vw-2rem))] rounded-2xl bg-white p-6 shadow-2xl sm:p-8">
                        <div className="mx-auto mb-5 flex h-16 w-16 items-center justify-center rounded-full bg-red-100">
                            <TriangleAlert
                                size={32}
                                className="text-red-600"
                            />
                        </div>

                        <h2 id="logout-title" className="text-center text-2xl font-bold text-gray-900">
                            Confirm Logout
                        </h2>

                        <p className="mt-3 text-center text-gray-500">
                            Are you sure you want to log out of your
                            CommuteShare account?
                        </p>

                        <div className="mt-8 flex justify-center gap-4">
                            <button
                                type="button"
                                onClick={() =>
                                    setShowLogoutModal(false)
                                }
                                className="rounded-xl border border-gray-300 px-6 py-2.5 font-medium text-gray-700 transition hover:bg-gray-100"
                            >
                                Cancel
                            </button>

                            <button
                                type="button"
                                onClick={confirmLogout}
                                className="rounded-xl bg-red-600 px-6 py-2.5 font-medium text-white transition hover:bg-red-700"
                            >
                                Logout
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </>
    );
}

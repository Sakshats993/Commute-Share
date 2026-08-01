import { useEffect, useRef, useState } from "react";
import {
    ChevronDown,
    LogOut,
    User,
    TriangleAlert,
} from "lucide-react";
import { useNavigate } from "react-router-dom";

import useAuth from "../../hooks/useAuth";
import ROUTES from "../../constants/routes";

export default function Navbar() {
    const { user, logout } = useAuth();
    const navigate = useNavigate();

    const [open, setOpen] = useState(false);
    const [showLogoutModal, setShowLogoutModal] = useState(false);

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
            <header className="bg-white shadow-sm border-b border-gray-200 px-8 py-4 flex justify-end items-center">
                <div className="relative" ref={menuRef}>
                    <button
                        onClick={() => setOpen(!open)}
                        className="flex items-center gap-3 rounded-xl px-3 py-2 hover:bg-gray-100 transition-all duration-200"
                    >
                        <div className="h-10 w-10 rounded-full bg-green-600 text-white flex items-center justify-center font-semibold text-lg">
                            {user?.full_name?.charAt(0).toUpperCase() || "U"}
                        </div>

                        <span className="font-semibold text-gray-800">
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
                        <div className="absolute right-0 mt-3 w-64 overflow-hidden rounded-2xl border border-gray-200 bg-white shadow-xl z-50">
                            <div className="border-b px-5 py-4">
                                <p className="font-semibold text-gray-900">
                                    {user?.full_name}
                                </p>

                                <p className="text-sm text-gray-500 truncate">
                                    {user?.email}
                                </p>
                            </div>

                            <button
                                onClick={handleProfile}
                                className="flex w-full items-center gap-3 px-5 py-3 text-gray-700 hover:bg-gray-100 transition"
                            >
                                <User size={18} />
                                My Profile
                            </button>

                            <button
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
                <div className="fixed inset-0 z-[100] flex items-center justify-center bg-black/40 backdrop-blur-sm">
                    <div className="w-[420px] rounded-2xl bg-white p-8 shadow-2xl animate-in fade-in zoom-in duration-200">
                        <div className="mx-auto mb-5 flex h-16 w-16 items-center justify-center rounded-full bg-red-100">
                            <TriangleAlert
                                size={32}
                                className="text-red-600"
                            />
                        </div>

                        <h2 className="text-center text-2xl font-bold text-gray-900">
                            Confirm Logout
                        </h2>

                        <p className="mt-3 text-center text-gray-500">
                            Are you sure you want to log out of your
                            CommuteShare account?
                        </p>

                        <div className="mt-8 flex justify-center gap-4">
                            <button
                                onClick={() =>
                                    setShowLogoutModal(false)
                                }
                                className="rounded-xl border border-gray-300 px-6 py-2.5 font-medium text-gray-700 transition hover:bg-gray-100"
                            >
                                Cancel
                            </button>

                            <button
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
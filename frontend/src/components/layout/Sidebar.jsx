import {
    Bell,
    Calendar,
    Car,
    Home,
    Shield,
    ShieldAlert,
    Star,
    User,
} from "lucide-react";

import { Link, NavLink } from "react-router-dom";
import { X } from "lucide-react";
import logo from "../../assets/images/logo.png";

import ROUTES from "../../constants/routes";
import useAuth from "../../hooks/useAuth";

const links = [
    {
        name: "Dashboard",
        icon: Home,
        path: ROUTES.DASHBOARD,
    },
    {
        name: "Rides",
        icon: Car,
        path: ROUTES.RIDES,
    },
    {
        name: "Vehicles",
        icon: Car,
        path: ROUTES.VEHICLES,
        roles: ["driver"],
    },
    {
        name: "Bookings",
        icon: Calendar,
        path: ROUTES.BOOKINGS,
    },
    {
        name: "Notifications",
        icon: Bell,
        path: ROUTES.NOTIFICATIONS,
    },
    {
        name: "Ratings",
        icon: Star,
        path: ROUTES.RATINGS,
    },
    {
        name: "Profile",
        icon: User,
        path: ROUTES.PROFILE,
    },
    {
        name: "SOS",
        icon: ShieldAlert,
        path: ROUTES.SOS,
    },
    {
        name: "Admin",
        icon: Shield,
        path: ROUTES.ADMIN,
        roles: ["admin"],
    },
];

export default function Sidebar({ mobileOpen = false, onClose = () => {} }) {
    const { user } = useAuth();

    return (
        <aside
            id="primary-navigation"
            className={`fixed inset-y-0 left-0 z-50 w-72 overflow-y-auto bg-slate-900 text-white shadow-2xl transition-transform duration-200 lg:static lg:z-auto lg:min-h-screen lg:translate-x-0 ${
                mobileOpen ? "translate-x-0" : "-translate-x-full"
            }`}
            aria-label="Main navigation"
        >
            <button
                type="button"
                onClick={onClose}
                className="absolute right-3 top-3 rounded-lg p-2 text-slate-300 hover:bg-slate-800 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-white lg:hidden"
                aria-label="Close navigation"
            >
                <X size={20} aria-hidden="true" />
            </button>
            <Link
                to={ROUTES.DASHBOARD}
                onClick={onClose}
                aria-label="CommuteShare dashboard"
                className="flex items-center gap-3 border-b border-slate-700 p-5 transition-colors duration-200 hover:bg-slate-800"
            >
            <img
                src={logo}
                alt=""
                className="h-10 w-10 rounded-lg object-contain"
            />

            <div className="text-2xl font-extrabold tracking-tight">
            <span className="text-white">
                Commute
            </span>
            <span className="text-green-500">
                Share
            </span>
        </div>
    </Link>

            <nav className="px-4 py-5 space-y-2">
                {links
                    .filter((link) => {
                        if (!link.roles) return true;

                        return link.roles.includes(user?.role);
                    })
                    .map(({ name, icon: Icon, path }) => (
                        <NavLink
                            key={name}
                            to={path}
                            onClick={onClose}
                            className={({ isActive }) =>
                                `flex items-center gap-4 rounded-xl px-4 py-3 text-base font-medium transition-all duration-200 ${
                                    isActive
                                        ? "bg-slate-700 shadow-md"
                                        : "hover:bg-slate-800 hover:translate-x-1"
                                }`
                            }
                        >
                            <Icon size={18} />
                            {name}
                        </NavLink>
                    ))}
            </nav>
        </aside>
    );
}

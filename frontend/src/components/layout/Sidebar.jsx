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

export default function Sidebar() {
    const { user } = useAuth();

    return (
        <aside className="w-72 bg-slate-900 text-white min-h-screen shadow-2xl">
            <Link
                to={ROUTES.DASHBOARD}
                className="flex items-center gap-3 p-5 border-b border-slate-700 hover:bg-slate-800 transition-colors duration-200"
            >
            <img
                src={logo}
                alt="CommuteShare Logo"
                className="h-10 w-10     object-contain"
            />

            <div className="text-[30px] font-bold tracking-tight">
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
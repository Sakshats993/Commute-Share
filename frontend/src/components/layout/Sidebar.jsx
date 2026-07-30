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

import { NavLink } from "react-router-dom";

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
        <aside className="w-64 bg-slate-900 text-white min-h-screen">
            <div className="p-6 text-2xl font-bold border-b border-slate-700">
                CommuteShare
            </div>

            <nav className="p-4 space-y-2">
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
                                `flex items-center gap-3 p-3 rounded transition ${
                                    isActive
                                        ? "bg-slate-700"
                                        : "hover:bg-slate-800"
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
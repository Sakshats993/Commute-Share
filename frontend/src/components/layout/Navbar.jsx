import { LogOut } from "lucide-react";
import { useNavigate } from "react-router-dom";

import useAuth from "../../hooks/useAuth";
import ROUTES from "../../constants/routes";

export default function Navbar() {
    const { user, logout } = useAuth();
    const navigate = useNavigate();

    function handleLogout() {
        logout();
        navigate(ROUTES.LOGIN);
    }

    return (
        <header className="bg-white shadow px-6 py-4 flex justify-between items-center">
            <div>
                <h1 className="text-2xl font-bold">
                    CommuteShare
                </h1>
            </div>

            <div className="flex items-center gap-4">
                <span className="font-medium">
                    {user?.full_name}
                </span>

                <button
                    onClick={handleLogout}
                    className="flex items-center gap-2 bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg transition"
                >
                    <LogOut size={18} />
                    Logout
                </button>
            </div>
        </header>
    );
}
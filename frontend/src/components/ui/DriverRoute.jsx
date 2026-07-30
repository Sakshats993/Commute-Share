import { Navigate } from "react-router-dom";

import useAuth from "../../hooks/useAuth";
import ROUTES from "../../constants/routes";
import ROLES from "../../constants/roles";
import LoadingSpinner from "./LoadingSpinner";

export default function DriverRoute({ children }) {
    const {
        authenticated,
        loading,
        user,
    } = useAuth();

    if (loading) {
        return (
            <div className="min-h-screen flex items-center justify-center bg-slate-100">
                <LoadingSpinner />
            </div>
        );
    }

    if (!authenticated) {
        return (
            <Navigate
                to={ROUTES.LOGIN}
                replace
            />
        );
    }

    if (!user) {
        return (
            <Navigate
                to={ROUTES.LOGIN}
                replace
            />
        );
    }

    const allowedRoles = [
        ROLES.DRIVER,
        ROLES.ADMIN,
    ];

    if (!allowedRoles.includes(user.role)) {
        return (
            <Navigate
                to={ROUTES.DASHBOARD}
                replace
            />
        );
    }

    return children;
}
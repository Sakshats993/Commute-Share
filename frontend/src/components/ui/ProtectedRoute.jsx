import { Navigate } from "react-router-dom";

import useAuth from "../../hooks/useAuth";
import ROUTES from "../../constants/routes";
import LoadingSpinner from "./LoadingSpinner";

export default function ProtectedRoute({ children }) {
    const { authenticated, loading } = useAuth();

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

    return children;
}
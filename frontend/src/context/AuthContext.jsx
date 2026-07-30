import {
    createContext,
    useEffect,
    useState,
} from "react";

import * as authApi from "../api/auth";
import authStore from "../store/authStore";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
    const [user, setUser] = useState(authStore.user);

    const [loading, setLoading] = useState(true);

    const [authenticated, setAuthenticated] = useState(
        authStore.isAuthenticated()
    );

    useEffect(() => {
        initializeAuth();
    }, []);

    async function initializeAuth() {
        if (!authStore.isAuthenticated()) {
            setLoading(false);
            return;
        }

        try {
            const currentUser =
                await authApi.getCurrentUser();

            authStore.updateUser(currentUser);

            setUser(currentUser);

            setAuthenticated(true);
        } catch (error) {
            console.error(
                "Authentication initialization failed:",
                error
            );

            authStore.logout();

            setUser(null);

            setAuthenticated(false);
        } finally {
            setLoading(false);
        }
    }

    async function login(email, password) {
        try {
            const response =
                await authApi.login(email, password);

            authStore.setAuth(
                response.access_token,
                null
            );

            const currentUser =
                await authApi.getCurrentUser();

            authStore.updateUser(currentUser);

            setUser(currentUser);

            setAuthenticated(true);

            return currentUser;
        } catch (error) {
            authStore.logout();

            setUser(null);

            setAuthenticated(false);

            throw error;
        }
    }

    async function register(userData) {
        return await authApi.register(userData);
    }

    function logout() {
        authStore.logout();

        setUser(null);

        setAuthenticated(false);
    }

    async function refreshUser() {
        try {
            const currentUser =
                await authApi.getCurrentUser();

            authStore.updateUser(currentUser);

            setUser(currentUser);

            return currentUser;
        } catch (error) {
            logout();
            throw error;
        }
    }

    const value = {
        user,
        loading,
        authenticated,
        login,
        register,
        logout,
        refreshUser,
    };

    return (
        <AuthContext.Provider value={value}>
            {children}
        </AuthContext.Provider>
    );
}

export default AuthContext;
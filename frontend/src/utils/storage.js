const ACCESS_TOKEN_KEY = "access_token";
const USER_KEY = "user";

export const storage = {
    getToken() {
        return localStorage.getItem(ACCESS_TOKEN_KEY);
    },

    setToken(token) {
        localStorage.setItem(ACCESS_TOKEN_KEY, token);
    },

    removeToken() {
        localStorage.removeItem(ACCESS_TOKEN_KEY);
    },

    getUser() {
        const user = localStorage.getItem(USER_KEY);

        if (!user) return null;

        try {
            return JSON.parse(user);
        } catch {
            return null;
        }
    },

    setUser(user) {
        localStorage.setItem(
            USER_KEY,
            JSON.stringify(user)
        );
    },

    removeUser() {
        localStorage.removeItem(USER_KEY);
    },

    clear() {
        localStorage.removeItem(ACCESS_TOKEN_KEY);
        localStorage.removeItem(USER_KEY);
    },
};  
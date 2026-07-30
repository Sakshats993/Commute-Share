import { storage } from "../utils/storage";

class AuthStore {
    constructor() {
        this.token = storage.getToken();
        this.user = storage.getUser();
    }

    isAuthenticated() {
        return Boolean(this.token);
    }

    setAuth(token, user = null) {
        this.token = token;
        this.user = user;

        storage.setToken(token);

        if (user) {
            storage.setUser(user);
        }
    }

    updateUser(user) {
        this.user = user;
        storage.setUser(user);
    }

    logout() {
        this.token = null;
        this.user = null;

        storage.clear();
    }

    getToken() {
        return this.token;
    }

    getUser() {
        return this.user;
    }
}

const authStore = new AuthStore();

export default authStore;
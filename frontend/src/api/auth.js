import api from "./axios";

/*
------------------------------------
Register
POST /auth/register
(JSON)
------------------------------------
*/

export async function register(userData) {
    const response = await api.post(
        "/auth/register",
        userData
    );

    return response.data;
}

/*
------------------------------------
Login
POST /auth/login
(Form Data)
------------------------------------
*/

export async function login(email, password) {
    const formData = new URLSearchParams();

    formData.append("username", email);
    formData.append("password", password);

    const response = await api.post(
        "/auth/login",
        formData,
        {
            headers: {
                "Content-Type":
                    "application/x-www-form-urlencoded",
            },
        }
    );

    return response.data;
}

/*
------------------------------------
Current User
------------------------------------
*/

export async function getCurrentUser() {
    const response = await api.get("/auth/me");

    return response.data;
}

/*
------------------------------------
Change Password
------------------------------------
*/

export async function changePassword(data) {
    await api.put(
        "/auth/change-password",
        data
    );
}

export async function requestPasswordReset(email) {
    const response = await api.post("/auth/password-reset/request", { email });
    return response.data;
}

export async function confirmPasswordReset(token, newPassword) {
    await api.post("/auth/password-reset/confirm", {
        token,
        new_password: newPassword,
    });
}

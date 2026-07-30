import api from "./axios";

export async function getDashboardStatistics() {
    const response = await api.get(
        "/admin/dashboard"
    );

    return response.data;
}

export async function getUsers() {
    const response = await api.get(
        "/admin/users"
    );

    return response.data;
}

export async function getRides() {
    const response = await api.get(
        "/admin/rides"
    );

    return response.data;
}

export async function getBookings() {
    const response = await api.get(
        "/admin/bookings"
    );

    return response.data;
}

export async function activateUser(userId) {
    const response = await api.patch(
        `/admin/users/${userId}/activate`
    );

    return response.data;
}

export async function deactivateUser(userId) {
    const response = await api.patch(
        `/admin/users/${userId}/deactivate`
    );

    return response.data;
}
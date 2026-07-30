import api from "./axios";

export async function triggerSOS(data) {
    const response = await api.post(
        "/sos",
        data
    );

    return response.data;
}

export async function getMySOSEvents() {
    const response = await api.get(
        "/sos/me"
    );

    return response.data;
}

export async function getSOSDetails(id) {
    const response = await api.get(
        `/sos/${id}`
    );

    return response.data;
}
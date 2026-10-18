import api from "./axios";

export async function getRides() {
    const response = await api.get("/rides");
    return response.data;
}

export async function getRide(rideId) {
    const response = await api.get(`/rides/${rideId}`);
    return response.data;
}

export async function createRide(rideData) {
    const response = await api.post("/rides/", rideData);
    return response.data;
}

export async function updateRide(rideId, rideData) {
    const response = await api.put(
        `/rides/${rideId}`,
        rideData
    );

    return response.data;
}

export async function deleteRide(rideId) {
    await api.delete(`/rides/${rideId}`);
}

export async function searchRides(filters) {
    const params = Object.fromEntries(
        Object.entries(filters).filter(([, value]) => value !== "" && value != null)
    );
    const response = await api.get("/rides/search", {
        params,
    });

    return response.data;
}
export async function startRide(rideId) {
    const response = await api.patch(
        `/rides/${rideId}/start`
    );

    return response.data;
}
export async function confirmRide(rideId) {
    const response = await api.patch(
        `/rides/${rideId}/confirm`
    );

    return response.data;
}

export async function endRide(rideId) {
    const response = await api.patch(
        `/rides/${rideId}/end`
    );

    return response.data;
}

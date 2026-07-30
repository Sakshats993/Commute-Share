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
    const response = await api.post("/rides", rideData);
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

export async function searchRides(
    source,
    destination
) {
    const response = await api.get("/rides/search", {
        params: {
            source,
            destination,
        },
    });

    return response.data;
}
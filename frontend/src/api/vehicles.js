import api from "./axios";

export async function getVehicles() {
    const response = await api.get("/vehicles");

    return response.data;
}

export async function getVehicle(vehicleId) {
    const response = await api.get(
        `/vehicles/${vehicleId}`
    );

    return response.data;
}

export async function createVehicle(vehicleData) {
    const response = await api.post(
        "/vehicles",
        vehicleData
    );

    return response.data;
}

export async function updateVehicle(
    vehicleId,
    vehicleData
) {
    const response = await api.put(
        `/vehicles/${vehicleId}`,
        vehicleData
    );

    return response.data;
}

export async function deleteVehicle(vehicleId) {
    await api.delete(`/vehicles/${vehicleId}`);
}
import { useEffect, useState } from "react";

import * as vehicleApi from "../api/vehicles";

export default function useVehicles() {
    const [vehicles, setVehicles] = useState([]);

    const [loading, setLoading] = useState(true);

    const [error, setError] = useState(null);

    async function loadVehicles() {
        try {
            setLoading(true);

            const data =
                await vehicleApi.getVehicles();

            setVehicles(data);

            setError(null);
        } catch (err) {
            setError(err);
        } finally {
            setLoading(false);
        }
    }

    async function addVehicle(vehicle) {
        const newVehicle =
            await vehicleApi.createVehicle(vehicle);

        setVehicles((prev) => [
            ...prev,
            newVehicle,
        ]);
    }

    async function editVehicle(id, data) {
        const updated =
            await vehicleApi.updateVehicle(
                id,
                data
            );

        setVehicles((prev) =>
            prev.map((vehicle) =>
                vehicle.id === id
                    ? updated
                    : vehicle
            )
        );
    }

    async function removeVehicle(id) {
        await vehicleApi.deleteVehicle(id);

        setVehicles((prev) =>
            prev.filter(
                (vehicle) => vehicle.id !== id
            )
        );
    }

    useEffect(() => {
        loadVehicles();
    }, []);

    return {
        vehicles,

        loading,

        error,

        loadVehicles,

        addVehicle,

        editVehicle,

        removeVehicle,
    };
}
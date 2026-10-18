import { useEffect, useState } from "react";

import * as rideApi from "../api/rides";

export default function useRides() {
    const [rides, setRides] = useState([]);

    const [loading, setLoading] = useState(true);

    const [error, setError] = useState(null);

    async function loadRides() {
        try {
            setLoading(true);
            setError(null);

            const data =
                await rideApi.getRides();

            setRides(data);

            setError(null);
        } catch (err) {
            setError(err);
        } finally {
            setLoading(false);
        }
    }

    async function search(filters = {}) {
        const activeFilters = Object.fromEntries(
            Object.entries(filters).filter(([key, value]) => key !== "sort_by" && value !== "" && value != null)
        );
        if (Object.keys(activeFilters).length === 0 && filters.sort_by !== "price") {
            await loadRides();
            return;
        }

        try {
            setLoading(true);
            setError(null);

            const data =
                await rideApi.searchRides(
                    filters
                );

            setRides(data);
        } catch (err) {
            setError(err);
            setRides([]);
        } finally {
            setLoading(false);
        }
    }

    async function addRide(data) {
        try {
            const newRide = await rideApi.createRide(data);
            setError(null);
            setRides((prev) => [newRide, ...prev]);
        } catch (err) {
            throw err;
        }
    }

    async function editRide(
        id,
        data
    ) {
        try {
            const updated = await rideApi.updateRide(id, data);
            setError(null);
            setRides((prev) =>
                prev.map((ride) => (ride.id === id ? updated : ride))
            );
        } catch (err) {
            throw err;
        }
    }

    async function removeRide(id) {
        try {
            await rideApi.deleteRide(id);
            setError(null);
            setRides((prev) => prev.filter((ride) => ride.id !== id));
        } catch (err) {
            throw err;
        }
    }

    useEffect(() => {
        loadRides();
    }, []);

    return {
        rides,
        loading,
        error,
        loadRides,
        search,
        addRide,
        editRide,
        removeRide,
    };
}

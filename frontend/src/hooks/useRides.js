import { useEffect, useState } from "react";

import * as rideApi from "../api/rides";

export default function useRides() {
    const [rides, setRides] = useState([]);

    const [loading, setLoading] = useState(true);

    const [error, setError] = useState(null);

    async function loadRides() {
        try {
            setLoading(true);

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

    async function search(
        source,
        destination
    ) {
        try {
            setLoading(true);

            const data =
                await rideApi.searchRides(
                    source,
                    destination
                );

            setRides(data);
        } finally {
            setLoading(false);
        }
    }

    async function addRide(data) {
        const newRide =
            await rideApi.createRide(data);

        setRides((prev) => [
            newRide,
            ...prev,
        ]);
    }

    async function editRide(
        id,
        data
    ) {
        const updated =
            await rideApi.updateRide(
                id,
                data
            );

        setRides((prev) =>
            prev.map((ride) =>
                ride.id === id
                    ? updated
                    : ride
            )
        );
    }

    async function removeRide(id) {
        await rideApi.deleteRide(id);

        setRides((prev) =>
            prev.filter(
                (ride) =>
                    ride.id !== id
            )
        );
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
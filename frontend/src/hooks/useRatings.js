import { useState } from "react";

import * as ratingApi from "../api/ratings";

export default function useRatings() {
    const [ratings, setRatings] = useState([]);

    const [loading, setLoading] = useState(false);

    const [error, setError] = useState(null);

    async function loadRatings(userId) {
        try {
            setLoading(true);

            const data =
                await ratingApi.getUserRatings(userId);

            setRatings(data);

            setError(null);
        } catch (err) {
            setError(err);
            throw err;
        } finally {
            setLoading(false);
        }
    }

    async function addRating(data) {
        try {
            const rating =
                await ratingApi.createRating(data);

            setRatings((prev) => [
                rating,
                ...prev,
            ]);

            setError(null);

            return rating;
        } catch (err) {
            setError(err);
            throw err;
        }
    }

    async function editRating(id, data) {
        try {
            const updated =
                await ratingApi.updateRating(
                    id,
                    data
                );

            setRatings((prev) =>
                prev.map((rating) =>
                    rating.id === id
                        ? updated
                        : rating
                )
            );

            setError(null);

            return updated;
        } catch (err) {
            setError(err);
            throw err;
        }
    }

    async function removeRating(id) {
        try {
            await ratingApi.deleteRating(id);

            setRatings((prev) =>
                prev.filter(
                    (rating) => rating.id !== id
                )
            );

            setError(null);
        } catch (err) {
            setError(err);
            throw err;
        }
    }

    return {
        ratings,
        loading,
        error,
        loadRatings,
        addRating,
        editRating,
        removeRating,
    };
}
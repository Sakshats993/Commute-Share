import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import toast from "react-hot-toast";

import Layout from "../components/ui/Layout";
import LoadingSpinner from "../components/ui/LoadingSpinner";
import EmptyState from "../components/ui/EmptyState";

import RatingForm from "../components/ratings/RatingForm";
import RatingList from "../components/ratings/RatingList";

import useRatings from "../hooks/useRatings";

export default function RatingsPage() {
    const { userId } = useParams();

    const {
        ratings,
        loading,
        loadRatings,
        addRating,
        editRating,
        removeRating,
    } = useRatings();

    const [selectedRating, setSelectedRating] =
        useState(null);

    const [submitting, setSubmitting] =
        useState(false);

    useEffect(() => {
        loadRatings(userId);
    }, [userId]);

    async function handleSubmit(data) {
        try {
            setSubmitting(true);

            if (selectedRating) {
                await editRating(
                    selectedRating.id,
                    data
                );

                toast.success(
                    "Rating updated successfully."
                );
            } else {
                await addRating(data);

                toast.success(
                    "Rating submitted successfully."
                );
            }

            setSelectedRating(null);
        } catch (error) {
            toast.error(
                error.response?.data?.detail ??
                    "Operation failed."
            );
        } finally {
            setSubmitting(false);
        }
    }

    async function handleDelete(rating) {
        if (
            !window.confirm(
                "Delete this rating?"
            )
        ) {
            return;
        }

        try {
            await removeRating(rating.id);

            toast.success(
                "Rating deleted successfully."
            );
        } catch (error) {
            toast.error(
                error.response?.data?.detail ??
                    "Unable to delete rating."
            );
        }
    }

    if (loading) {
        return (
            <Layout>
                <LoadingSpinner />
            </Layout>
        );
    }

    return (
        <Layout>
            <div className="space-y-6">

                <h1 className="text-3xl font-bold">
                    Ratings
                </h1>

                <RatingForm
                    initialValues={selectedRating}
                    onSubmit={handleSubmit}
                    submitting={submitting}
                />

                {ratings.length === 0 ? (
                    <EmptyState
                        title="No Ratings"
                        description="No ratings have been submitted yet."
                    />
                ) : (
                    <RatingList
                        ratings={ratings}
                        onEdit={setSelectedRating}
                        onDelete={handleDelete}
                    />
                )}

            </div>
        </Layout>
    );
}
import { useEffect, useState } from "react";
import toast from "react-hot-toast";

import Layout from "../components/ui/Layout";
import LoadingSpinner from "../components/ui/LoadingSpinner";
import EmptyState from "../components/ui/EmptyState";

import RatingForm from "../components/ratings/RatingForm";
import RatingList from "../components/ratings/RatingList";

import useRatings from "../hooks/useRatings";

export default function RatingsPage() {
    const {
        ratings,
        candidates,
        loading,
        loadRatings,
        loadCandidates,
        addRating,
        editRating,
        removeRating,
    } = useRatings();

    const [selectedCandidate, setSelectedCandidate] =
        useState(null);

    const [selectedRating, setSelectedRating] =
        useState(null);

    const [submitting, setSubmitting] =
        useState(false);

    useEffect(() => {
        async function load() {
            try {
                await Promise.all([
                    loadRatings(),
                    loadCandidates(),
                ]);
            } catch {
                toast.error(
                    "Unable to load ratings."
                );
            }
        }

        load();
    }, []);

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

                setSelectedRating(null);
            } else {
                await addRating({
                    booking_id:
                        selectedCandidate.booking_id,
                    rating: data.rating,
                    review: data.review,
                });

                toast.success(
                    "Rating submitted successfully."
                );

                setSelectedCandidate(null);

                await loadCandidates();
                await loadRatings();
            }
        } catch (error) {
            toast.error(
                error.response?.data?.detail ??
                    "Unable to submit rating."
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

            await loadRatings();
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
                <div className="flex justify-center py-24">
                    <LoadingSpinner />
                </div>
            </Layout>
        );
    }

    return (
        <Layout>
            <div className="space-y-8">

                {/* Header */}
                <div>
                    <h1 className="text-4xl font-bold text-gray-900">
                        Ratings
                    </h1>

                    <p className="mt-2 text-gray-500">
                        Rate people you've shared a completed ride with
                        and view your ratings.
                    </p>
                </div>

                {/* Rating form */}
                {selectedCandidate && (
                    <RatingForm
                        candidate={selectedCandidate}
                        onSubmit={handleSubmit}
                        submitting={submitting}
                    />
                )}

                {/* Pending ratings */}
                <section>
                    <div className="mb-4">
                        <h2 className="text-2xl font-bold text-gray-900">
                            {candidates.length > 0
                                ? candidates[0].reviewee_role ===
                                  "driver"
                                    ? "Rate Your Drivers"
                                    : "Rate Your Passengers"
                                : "Completed Rides"}
                        </h2>

                        <p className="mt-1 text-gray-500">
                            Share your experience after a completed ride.
                        </p>
                    </div>

                    {candidates.length === 0 ? (
                        <div className="bg-white rounded-2xl border border-gray-200 p-8">
                            <p className="text-center text-gray-500">
                                No completed rides are waiting for a rating.
                            </p>
                        </div>
                    ) : (
                        <div className="grid gap-4">
                            {candidates.map((candidate) => (
                                <div
                                    key={candidate.booking_id}
                                    className="bg-white rounded-2xl border border-gray-200 shadow-sm p-6"
                                >
                                    <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">

                                        <div>
                                            <p className="text-sm text-gray-500">
                                                {candidate.reviewee_role ===
                                                "driver"
                                                    ? "Driver"
                                                    : "Passenger"}
                                            </p>

                                            <h3 className="text-xl font-semibold text-gray-900">
                                                {
                                                    candidate.reviewee_name
                                                }
                                            </h3>

                                            <p className="mt-1 text-gray-600">
                                                {
                                                    candidate.pickup_location
                                                }
                                                {" → "}
                                                {
                                                    candidate.destination_location
                                                }
                                            </p>

                                            <p className="mt-1 text-sm text-gray-400">
                                                {new Date(
                                                    candidate.departure_time
                                                ).toLocaleString()}
                                            </p>
                                        </div>

                                        <button
                                            onClick={() =>
                                                setSelectedCandidate(
                                                    candidate
                                                )
                                            }
                                            className="bg-blue-600 hover:bg-blue-700 text-white px-5 py-3 rounded-lg font-medium"
                                        >
                                            {candidate.reviewee_role ===
                                            "driver"
                                                ? "Rate Driver"
                                                : "Rate Passenger"}
                                        </button>
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}
                </section>

                {/* Received ratings */}
                <section>
                    <div className="mb-4">
                        <h2 className="text-2xl font-bold text-gray-900">
                            Ratings You've Received
                        </h2>

                        <p className="mt-1 text-gray-500">
                            See what other passengers and drivers think
                            about you.
                        </p>
                    </div>

                    {ratings.length === 0 ? (
                        <div className="bg-white rounded-2xl border border-gray-200 p-8">
                            <p className="text-center text-gray-500">
                                You haven't received any ratings yet.
                            </p>
                        </div>
                    ) : (
                        <RatingList
                            ratings={ratings}
                            onEdit={setSelectedRating}
                            onDelete={handleDelete}
                        />
                    )}
                </section>

            </div>
        </Layout>
    );
}
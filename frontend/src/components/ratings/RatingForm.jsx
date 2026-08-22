import { useEffect, useState } from "react";

const initialState = {
    rating: 5,
    review: "",
};

export default function RatingForm({
    candidate,
    initialValues,
    onSubmit,
    submitting,
}) {
    const [formData, setFormData] =
        useState(initialState);

    useEffect(() => {
        if (initialValues) {
            setFormData({
                rating:
                    initialValues.rating ?? 5,
                review:
                    initialValues.review ?? "",
            });
        } else {
            setFormData(initialState);
        }
    }, [initialValues]);

    function handleChange(e) {
        const { name, value } = e.target;

        setFormData((prev) => ({
            ...prev,
            [name]:
                name === "rating"
                    ? Number(value)
                    : value,
        }));
    }

    function handleSubmit(e) {
        e.preventDefault();

        if (!candidate && !initialValues) {
            return;
        }

        onSubmit(formData);
    }

    if (!candidate && !initialValues) {
        return null;
    }

    const role =
        candidate?.reviewee_role ??
        "user";

    const title =
        role === "driver"
            ? "Rate Your Driver"
            : "Rate Your Passenger";

    const personLabel =
        role === "driver"
            ? "Driver"
            : "Passenger";

    return (
        <form
            onSubmit={handleSubmit}
            className="bg-white rounded-2xl border border-gray-200 shadow-sm p-6 space-y-5"
        >
            <div>
                <h2 className="text-2xl font-bold text-gray-900">
                    {title}
                </h2>

                {candidate && (
                    <div className="mt-3 rounded-xl bg-gray-50 p-4">
                        <p className="text-sm text-gray-500">
                            {personLabel}
                        </p>

                        <p className="text-lg font-semibold text-gray-900">
                            {candidate.reviewee_name}
                        </p>

                        <p className="mt-1 text-sm text-gray-500">
                            {candidate.pickup_location}
                            {" → "}
                            {candidate.destination_location}
                        </p>
                    </div>
                )}
            </div>

            <div>
                <label className="block mb-2 font-medium text-gray-900">
                    Rating
                </label>

                <select
                    name="rating"
                    value={formData.rating}
                    onChange={handleChange}
                    className="w-full border border-gray-300 rounded-lg p-3"
                >
                    {[5, 4, 3, 2, 1].map((star) => (
                        <option
                            key={star}
                            value={star}
                        >
                            {"★".repeat(star)}
                            {" "}
                            {star} Star
                        </option>
                    ))}
                </select>
            </div>

            <div>
                <label className="block mb-2 font-medium text-gray-900">
                    Your Review
                </label>

                <textarea
                    name="review"
                    rows={4}
                    value={formData.review}
                    onChange={handleChange}
                    placeholder={`Write a review about the ${role}...`}
                    className="w-full border border-gray-300 rounded-lg p-3"
                />
            </div>

            <button
                type="submit"
                disabled={submitting}
                className="bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white px-5 py-3 rounded-lg"
            >
                {submitting
                    ? "Submitting..."
                    : initialValues
                    ? "Update Rating"
                    : "Submit Rating"}
            </button>
        </form>
    );
}
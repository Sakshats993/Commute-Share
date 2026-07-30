import { useEffect, useState } from "react";

const initialState = {
    ride_id: "",
    reviewee_id: "",
    rating: 5,
    review: "",
};

export default function RatingForm({
    initialValues,
    onSubmit,
    submitting,
}) {
    const [formData, setFormData] =
        useState(initialState);

    useEffect(() => {
        if (initialValues) {
            setFormData({
                ride_id:
                    initialValues.ride_id ?? "",
                reviewee_id:
                    initialValues.reviewee_id ??
                    "",
                rating:
                    initialValues.rating ?? 5,
                review:
                    initialValues.review ?? "",
            });
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

        onSubmit(formData);
    }

    return (
        <form
            onSubmit={handleSubmit}
            className="bg-white rounded-xl shadow p-6 space-y-4"
        >
            {!initialValues && (
                <>
                    <div>
                        <label className="block mb-1 font-medium">
                            Ride ID
                        </label>

                        <input
                            type="number"
                            name="ride_id"
                            value={formData.ride_id}
                            onChange={handleChange}
                            required
                            className="w-full border rounded-lg p-3"
                        />
                    </div>

                    <div>
                        <label className="block mb-1 font-medium">
                            Reviewee ID
                        </label>

                        <input
                            type="number"
                            name="reviewee_id"
                            value={
                                formData.reviewee_id
                            }
                            onChange={handleChange}
                            required
                            className="w-full border rounded-lg p-3"
                        />
                    </div>
                </>
            )}

            <div>
                <label className="block mb-1 font-medium">
                    Rating
                </label>

                <select
                    name="rating"
                    value={formData.rating}
                    onChange={handleChange}
                    className="w-full border rounded-lg p-3"
                >
                    {[1, 2, 3, 4, 5].map((star) => (
                        <option
                            key={star}
                            value={star}
                        >
                            {star} Star
                        </option>
                    ))}
                </select>
            </div>

            <div>
                <label className="block mb-1 font-medium">
                    Review
                </label>

                <textarea
                    name="review"
                    rows={4}
                    value={formData.review}
                    onChange={handleChange}
                    className="w-full border rounded-lg p-3"
                />
            </div>

            <button
                type="submit"
                disabled={submitting}
                className="bg-blue-600 hover:bg-blue-700 text-white px-5 py-3 rounded-lg"
            >
                {submitting
                    ? "Saving..."
                    : initialValues
                    ? "Update Rating"
                    : "Submit Rating"}
            </button>
        </form>
    );
}
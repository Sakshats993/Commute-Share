import { useEffect, useState } from "react";

const initialState = {
    make: "",
    model: "",
    color: "",
    registration_number: "",
    seating_capacity: 4,
    is_active: true,
};

export default function VehicleForm({
    initialData,
    onSubmit,
    onCancel,
}) {
    const [form, setForm] =
        useState(initialState);

    useEffect(() => {
        if (initialData) {
            setForm({
                ...initialData,
            });
        }
    }, [initialData]);

    function handleChange(e) {
        const { name, value, type, checked } =
            e.target;

        setForm((prev) => ({
            ...prev,
            [name]:
                type === "checkbox"
                    ? checked
                    : value,
        }));
    }

    function handleSubmit(e) {
        e.preventDefault();

        const payload = { ...form };

        if (initialData) {
            delete payload.registration_number;
        }

        onSubmit(payload);
    }

    return (
        <form
            onSubmit={handleSubmit}
            className="space-y-4"
        >
            <input
                name="make"
                placeholder="Make"
                value={form.make}
                onChange={handleChange}
                className="w-full border rounded-lg p-3"
                required
            />

            <input
                name="model"
                placeholder="Model"
                value={form.model}
                onChange={handleChange}
                className="w-full border rounded-lg p-3"
                required
            />

            <input
                name="color"
                placeholder="Color"
                value={form.color}
                onChange={handleChange}
                className="w-full border rounded-lg p-3"
                required
            />

            {!initialData && (
                <input
                    name="registration_number"
                    placeholder="Registration Number"
                    value={
                        form.registration_number
                    }
                    onChange={handleChange}
                    className="w-full border rounded-lg p-3"
                    required
                />
            )}

            <input
                type="number"
                name="seating_capacity"
                min="1"
                max="10"
                value={form.seating_capacity}
                onChange={handleChange}
                className="w-full border rounded-lg p-3"
                required
            />

            {initialData && (
                <label className="flex gap-2 items-center">
                    <input
                        type="checkbox"
                        name="is_active"
                        checked={form.is_active}
                        onChange={handleChange}
                    />

                    Active Vehicle
                </label>
            )}

            <div className="flex gap-3">
                <button
                    type="submit"
                    className="bg-blue-600 text-white px-5 py-2 rounded-lg"
                >
                    {initialData
                        ? "Update"
                        : "Create"}
                </button>

                <button
                    type="button"
                    onClick={onCancel}
                    className="bg-gray-300 px-5 py-2 rounded-lg"
                >
                    Cancel
                </button>
            </div>
        </form>
    );
}
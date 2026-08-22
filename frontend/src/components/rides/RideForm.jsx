import { useEffect, useState } from "react";

import { getVehicles } from "../../api/vehicles";

const initialForm = {
    vehicle_make: "",
    vehicle_model: "",
    vehicle_color: "",
    registration_number: "",
    vehicle_seating_capacity: 4,

    pickup_location: "",
    pickup_latitude: "",
    pickup_longitude: "",
    destination_location: "",
    destination_latitude: "",
    destination_longitude: "",
    departure_time: "",
    estimated_arrival_time: "",
    total_seats: 1,
    price_per_seat: "",
    notes: "",
};

const inputClass =
    "w-full rounded-xl border border-gray-300 px-4 py-3 outline-none transition focus:border-blue-500 focus:ring-2 focus:ring-blue-200";

export default function RideForm({
    initialData,
    onSubmit,
    onCancel,
}) {
    const [form, setForm] = useState(initialForm);
    const [vehicles, setVehicles] = useState([]);

    useEffect(() => {
        loadVehicles();

        if (initialData) {
            setForm({
                ...initialData,
            });
        } else {
            setForm(initialForm);
        }
    }, [initialData]);

    async function loadVehicles() {
    try {
        const data = await getVehicles();

        console.log("Vehicles API response:", data);

        setVehicles(data);
    } catch (error) {
        console.error("Failed to load vehicles:", error);
        }
    }

    function handleChange(e) {
        const { name, value } = e.target;

        setForm((prev) => ({
            ...prev,
            [name]: value,
        }));
    }

    function handleSubmit(e) {
        e.preventDefault();

        onSubmit({
            ...form,

            vehicle_seating_capacity: Number(
                form.vehicle_seating_capacity
            ),

            pickup_latitude: Number(
                form.pickup_latitude
            ),

            pickup_longitude: Number(
                form.pickup_longitude
            ),

            destination_latitude: Number(
                form.destination_latitude
            ),

            destination_longitude: Number(
                form.destination_longitude
            ),

            total_seats: Number(
                form.total_seats
            ),

            price_per_seat: Number(
                form.price_per_seat
            ),
        });
    }

    return (
        <form
            onSubmit={handleSubmit}
            className="space-y-8"
        >
            {/* Vehicle */}
            <section>
                <h3 className="mb-4 text-lg font-semibold text-gray-900">
                    Vehicle Information
                </h3>

                <div className="grid gap-4 md:grid-cols-2">

                    <input
                        name="vehicle_make"
                        placeholder="Vehicle Make"
                        value={form.vehicle_make}
                        onChange={handleChange}
                        className={inputClass}
                        required
                    />

                    <input
                        name="vehicle_model"
                        placeholder="Vehicle Model"
                        value={form.vehicle_model}
                        onChange={handleChange}
                        className={inputClass}
                        required
                    />

                    <input
                        name="vehicle_color"
                        placeholder="Vehicle Color"
                        value={form.vehicle_color}
                        onChange={handleChange}
                        className={inputClass}
                        required
                    />

                    <input
                        name="registration_number"
                        placeholder="Registration Number"
                        value={form.registration_number}
                        onChange={handleChange}
                        className={inputClass}
                        required
                    />

                    <input
                        type="number"
                        min="1"
                        max="10"
                        name="vehicle_seating_capacity"
                        placeholder="Vehicle Seating Capacity"
                        value={form.vehicle_seating_capacity}
                        onChange={handleChange}
                        className={inputClass}
                        required
                    />

                </div>
            </section>

            {/* Route */}
            <section>
                <h3 className="mb-4 text-lg font-semibold text-gray-900">
                    Route Details
                </h3>

                <div className="grid gap-4 md:grid-cols-2">
                    <input
                        name="pickup_location"
                        placeholder="Pickup Location"
                        value={form.pickup_location}
                        onChange={handleChange}
                        className={inputClass}
                        required
                    />

                    <input
                        name="destination_location"
                        placeholder="Destination Location"
                        value={form.destination_location}
                        onChange={handleChange}
                        className={inputClass}
                        required
                    />
                </div>
            </section>

            {/* Coordinates */}
            <section>
                <h3 className="mb-2 text-lg font-semibold text-gray-900">
                    Coordinates
                </h3>

                <p className="mb-4 text-sm text-gray-500">
                    Used for ride matching.
                </p>

                <div className="grid gap-4 md:grid-cols-2">
                    <input
                        type="number"
                        step="any"
                        name="pickup_latitude"
                        placeholder="Pickup Latitude"
                        value={form.pickup_latitude}
                        onChange={handleChange}
                        className={inputClass}
                        required
                    />

                    <input
                        type="number"
                        step="any"
                        name="pickup_longitude"
                        placeholder="Pickup Longitude"
                        value={form.pickup_longitude}
                        onChange={handleChange}
                        className={inputClass}
                        required
                    />

                    <input
                        type="number"
                        step="any"
                        name="destination_latitude"
                        placeholder="Destination Latitude"
                        value={form.destination_latitude}
                        onChange={handleChange}
                        className={inputClass}
                        required
                    />

                    <input
                        type="number"
                        step="any"
                        name="destination_longitude"
                        placeholder="Destination Longitude"
                        value={form.destination_longitude}
                        onChange={handleChange}
                        className={inputClass}
                        required
                    />
                </div>
            </section>

            {/* Schedule */}
            <section>
                <h3 className="mb-4 text-lg font-semibold text-gray-900">
                    Schedule
                </h3>

                <div className="grid gap-4 md:grid-cols-2">
                    <input
                        type="datetime-local"
                        name="departure_time"
                        value={form.departure_time}
                        onChange={handleChange}
                        className={inputClass}
                        required
                    />

                    <input
                        type="datetime-local"
                        name="estimated_arrival_time"
                        value={form.estimated_arrival_time}
                        onChange={handleChange}
                        className={inputClass}
                    />
                </div>
            </section>

            {/* Pricing */}
            <section>
                <h3 className="mb-4 text-lg font-semibold text-gray-900">
                    Seats & Pricing
                </h3>

                <div className="grid gap-4 md:grid-cols-2">
                    <input
                        type="number"
                        min="1"
                        max="10"
                        name="total_seats"
                        value={form.total_seats}
                        onChange={handleChange}
                        className={inputClass}
                        placeholder="Seats"
                        required
                    />

                    <input
                        type="number"
                        step="0.01"
                        min="0"
                        name="price_per_seat"
                        value={form.price_per_seat}
                        onChange={handleChange}
                        className={inputClass}
                        placeholder="Price Per Seat (₹)"
                        required
                    />
                </div>
            </section>

            {/* Notes */}
            <section>
                <h3 className="mb-4 text-lg font-semibold text-gray-900">
                    Additional Notes
                </h3>

                <textarea
                    rows="4"
                    name="notes"
                    placeholder="Example: Luggage allowed, Call before arrival, No smoking..."
                    value={form.notes}
                    onChange={handleChange}
                    className={inputClass}
                />
            </section>

            {/* Actions */}
            <div className="flex flex-wrap gap-4">
                <button
                    type="submit"
                    className="rounded-xl bg-blue-600 px-6 py-3 font-medium text-white transition hover:bg-blue-700"
                >
                    {initialData
                        ? "Update Ride"
                        : "Create Ride"}
                </button>

                <button
                    type="button"
                    onClick={onCancel}
                    className="rounded-xl border border-gray-300 px-6 py-3 font-medium text-gray-700 transition hover:bg-gray-100"
                >
                    Cancel
                </button>
            </div>
        </form>
    );
}
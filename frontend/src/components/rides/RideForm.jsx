import { useEffect, useState } from "react";


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

function toLocalDateTime(value) {
    if (!value) return "";
    const date = new Date(value);
    const local = new Date(date.getTime() - date.getTimezoneOffset() * 60_000);
    return local.toISOString().slice(0, 16);
}

export default function RideForm({
    initialData,
    onSubmit,
    onCancel,
}) {
    const [form, setForm] = useState(initialForm);
    useEffect(() => {
        if (initialData) {
            setForm({
                ...initialForm,
                vehicle_make: initialData.vehicle?.make ?? "",
                vehicle_model: initialData.vehicle?.model ?? "",
                vehicle_color: initialData.vehicle?.color ?? "",
                registration_number: initialData.vehicle?.registration_number ?? "",
                vehicle_seating_capacity: initialData.vehicle?.seating_capacity ?? 4,
                pickup_location: initialData.pickup_location ?? "",
                pickup_latitude: initialData.pickup_latitude ?? "",
                pickup_longitude: initialData.pickup_longitude ?? "",
                destination_location: initialData.destination_location ?? "",
                destination_latitude: initialData.destination_latitude ?? "",
                destination_longitude: initialData.destination_longitude ?? "",
                departure_time: toLocalDateTime(initialData.departure_time),
                estimated_arrival_time: toLocalDateTime(initialData.estimated_arrival_time),
                total_seats: initialData.total_seats ?? 1,
                price_per_seat: initialData.price_per_seat ?? "",
                notes: initialData.notes ?? "",
            });
        } else {
            setForm(initialForm);
        }
    }, [initialData]);

    function handleChange(e) {
        const { name, value } = e.target;

        setForm((prev) => ({
            ...prev,
            [name]: value,
        }));
    }

    function handleSubmit(e) {
        e.preventDefault();

        const routeAndRideFields = {
            pickup_location: form.pickup_location,
            pickup_latitude: Number(form.pickup_latitude),
            pickup_longitude: Number(form.pickup_longitude),
            destination_location: form.destination_location,
            destination_latitude: Number(form.destination_latitude),
            destination_longitude: Number(form.destination_longitude),
            departure_time: new Date(form.departure_time).toISOString(),
            estimated_arrival_time: form.estimated_arrival_time
                ? new Date(form.estimated_arrival_time).toISOString()
                : null,
            total_seats: Number(form.total_seats),
            price_per_seat: form.price_per_seat,
            notes: form.notes || null,
        };
        onSubmit(initialData ? routeAndRideFields : {
            ...routeAndRideFields,
            vehicle_make: form.vehicle_make,
            vehicle_model: form.vehicle_model,
            vehicle_color: form.vehicle_color,
            registration_number: form.registration_number,
            vehicle_seating_capacity: Number(form.vehicle_seating_capacity),
        });
    }

    return (
        <form
            onSubmit={handleSubmit}
            className="space-y-8"
        >
            {/* Vehicle */}
            {!initialData && <section>
                <h3 className="mb-4 text-lg font-semibold text-gray-900">
                    Vehicle Information
                </h3>

                <div className="grid gap-4 md:grid-cols-2">

                    <input
                        name="vehicle_make"
                        aria-label="Vehicle make"
                        placeholder="Vehicle Make"
                        value={form.vehicle_make}
                        onChange={handleChange}
                        className={inputClass}
                        required
                    />

                    <input
                        name="vehicle_model"
                        aria-label="Vehicle model"
                        placeholder="Vehicle Model"
                        value={form.vehicle_model}
                        onChange={handleChange}
                        className={inputClass}
                        required
                    />

                    <input
                        name="vehicle_color"
                        aria-label="Vehicle color"
                        placeholder="Vehicle Color"
                        value={form.vehicle_color}
                        onChange={handleChange}
                        className={inputClass}
                        required
                    />

                    <input
                        name="registration_number"
                        aria-label="Vehicle registration number"
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
                        aria-label="Vehicle seating capacity"
                        placeholder="Vehicle Seating Capacity"
                        value={form.vehicle_seating_capacity}
                        onChange={handleChange}
                        className={inputClass}
                        required
                    />

                </div>
            </section>}

            {/* Route */}
            <section>
                <h3 className="mb-4 text-lg font-semibold text-gray-900">
                    Route Details
                </h3>

                <div className="grid gap-4 md:grid-cols-2">
                    <input
                        name="pickup_location"
                        aria-label="Pickup location"
                        placeholder="Pickup Location"
                        value={form.pickup_location}
                        onChange={handleChange}
                        className={inputClass}
                        required
                    />

                    <input
                        name="destination_location"
                        aria-label="Destination location"
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
                        min="-90"
                        max="90"
                        name="pickup_latitude"
                        aria-label="Pickup latitude"
                        placeholder="Pickup Latitude"
                        value={form.pickup_latitude}
                        onChange={handleChange}
                        className={inputClass}
                        required
                    />

                    <input
                        type="number"
                        step="any"
                        min="-180"
                        max="180"
                        name="pickup_longitude"
                        aria-label="Pickup longitude"
                        placeholder="Pickup Longitude"
                        value={form.pickup_longitude}
                        onChange={handleChange}
                        className={inputClass}
                        required
                    />

                    <input
                        type="number"
                        step="any"
                        min="-90"
                        max="90"
                        name="destination_latitude"
                        aria-label="Destination latitude"
                        placeholder="Destination Latitude"
                        value={form.destination_latitude}
                        onChange={handleChange}
                        className={inputClass}
                        required
                    />

                    <input
                        type="number"
                        step="any"
                        min="-180"
                        max="180"
                        name="destination_longitude"
                        aria-label="Destination longitude"
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
                        aria-label="Departure time"
                        value={form.departure_time}
                        onChange={handleChange}
                        className={inputClass}
                        required
                    />

                    <input
                        type="datetime-local"
                        name="estimated_arrival_time"
                        aria-label="Estimated arrival time"
                        min={form.departure_time || undefined}
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
                        name="total_seats"
                        aria-label="Seats offered"
                        max={Math.min(10, Math.max(1, Number(form.vehicle_seating_capacity) - 1))}
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
                        aria-label="Price per seat"
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
                    aria-label="Additional ride notes"
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

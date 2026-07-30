import { useEffect, useState } from "react";

import { getVehicles } from "../../api/vehicles";

const initialForm = {
    vehicle_id: "",
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
        }
    }, [initialData]);

    async function loadVehicles() {
        const data = await getVehicles();
        setVehicles(data);
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

            vehicle_id: Number(form.vehicle_id),

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
            className="space-y-4"
        >
            <select
                name="vehicle_id"
                value={form.vehicle_id}
                onChange={handleChange}
                className="w-full border rounded-lg p-3"
                required
            >
                <option value="">
                    Select Vehicle
                </option>

                {vehicles.map((vehicle) => (
                    <option
                        key={vehicle.id}
                        value={vehicle.id}
                    >
                        {vehicle.make} {vehicle.model}
                        {" - "}
                        {
                            vehicle.registration_number
                        }
                    </option>
                ))}
            </select>

            <input
                name="pickup_location"
                placeholder="Pickup Location"
                value={form.pickup_location}
                onChange={handleChange}
                className="w-full border rounded-lg p-3"
                required
            />

            <input
                name="destination_location"
                placeholder="Destination Location"
                value={form.destination_location}
                onChange={handleChange}
                className="w-full border rounded-lg p-3"
                required
            />

            <div className="grid grid-cols-2 gap-4">
                <input
                    type="number"
                    step="any"
                    name="pickup_latitude"
                    placeholder="Pickup Latitude"
                    value={form.pickup_latitude}
                    onChange={handleChange}
                    className="border rounded-lg p-3"
                    required
                />

                <input
                    type="number"
                    step="any"
                    name="pickup_longitude"
                    placeholder="Pickup Longitude"
                    value={form.pickup_longitude}
                    onChange={handleChange}
                    className="border rounded-lg p-3"
                    required
                />

                <input
                    type="number"
                    step="any"
                    name="destination_latitude"
                    placeholder="Destination Latitude"
                    value={
                        form.destination_latitude
                    }
                    onChange={handleChange}
                    className="border rounded-lg p-3"
                    required
                />

                <input
                    type="number"
                    step="any"
                    name="destination_longitude"
                    placeholder="Destination Longitude"
                    value={
                        form.destination_longitude
                    }
                    onChange={handleChange}
                    className="border rounded-lg p-3"
                    required
                />
            </div>

            <input
                type="datetime-local"
                name="departure_time"
                value={form.departure_time}
                onChange={handleChange}
                className="w-full border rounded-lg p-3"
                required
            />

            <input
                type="datetime-local"
                name="estimated_arrival_time"
                value={
                    form.estimated_arrival_time
                }
                onChange={handleChange}
                className="w-full border rounded-lg p-3"
            />

            <div className="grid grid-cols-2 gap-4">
                <input
                    type="number"
                    min="1"
                    max="10"
                    name="total_seats"
                    value={form.total_seats}
                    onChange={handleChange}
                    className="border rounded-lg p-3"
                    required
                />

                <input
                    type="number"
                    step="0.01"
                    min="0"
                    name="price_per_seat"
                    value={form.price_per_seat}
                    onChange={handleChange}
                    className="border rounded-lg p-3"
                    placeholder="Price / Seat"
                    required
                />
            </div>

            <textarea
                rows="4"
                name="notes"
                placeholder="Notes"
                value={form.notes}
                onChange={handleChange}
                className="w-full border rounded-lg p-3"
            />

            <div className="flex gap-3">
                <button
                    className="bg-blue-600 text-white px-5 py-2 rounded-lg"
                >
                    {initialData
                        ? "Update Ride"
                        : "Create Ride"}
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
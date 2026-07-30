import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import toast from "react-hot-toast";

import Layout from "../components/ui/Layout";
import LoadingSpinner from "../components/ui/LoadingSpinner";

import { getRide } from "../api/rides";
import { bookRide } from "../api/bookings";

export default function RideDetailsPage() {
    const { rideId } = useParams();

    const [ride, setRide] = useState(null);
    const [loading, setLoading] = useState(true);
    const [bookingLoading, setBookingLoading] = useState(false);

    useEffect(() => {
        loadRide();
    }, []);

    async function loadRide() {
        try {
            setLoading(true);

            const data = await getRide(rideId);
            setRide(data);
        } catch (error) {
            toast.error(
                error.response?.data?.detail ??
                    "Failed to load ride."
            );
        } finally {
            setLoading(false);
        }
    }

    async function handleBookRide() {
        try {
            setBookingLoading(true);

            await bookRide(ride.id);

            toast.success("Ride booked successfully!");

            // Reload ride so available seats update
            await loadRide();
        } catch (error) {
            toast.error(
                error.response?.data?.detail ??
                    "Booking failed."
            );
        } finally {
            setBookingLoading(false);
        }
    }

    if (loading) {
        return (
            <Layout>
                <LoadingSpinner />
            </Layout>
        );
    }

    if (!ride) {
        return (
            <Layout>
                <div className="text-center mt-20 text-lg">
                    Ride not found.
                </div>
            </Layout>
        );
    }

    return (
        <Layout>
            <div className="max-w-4xl mx-auto bg-white rounded-xl shadow-lg p-8">

                <h1 className="text-3xl font-bold mb-8">
                    Ride Details
                </h1>

                <div className="grid md:grid-cols-2 gap-6">

                    <div>
                        <p className="font-semibold">
                            Pickup Location
                        </p>

                        <p className="text-gray-700">
                            {ride.pickup_location}
                        </p>
                    </div>

                    <div>
                        <p className="font-semibold">
                            Destination
                        </p>

                        <p className="text-gray-700">
                            {ride.destination_location}
                        </p>
                    </div>

                    <div>
                        <p className="font-semibold">
                            Departure Time
                        </p>

                        <p className="text-gray-700">
                            {new Date(
                                ride.departure_time
                            ).toLocaleString()}
                        </p>
                    </div>

                    <div>
                        <p className="font-semibold">
                            Estimated Arrival
                        </p>

                        <p className="text-gray-700">
                            {ride.estimated_arrival_time
                                ? new Date(
                                      ride.estimated_arrival_time
                                  ).toLocaleString()
                                : "Not specified"}
                        </p>
                    </div>

                    <div>
                        <p className="font-semibold">
                            Vehicle ID
                        </p>

                        <p>{ride.vehicle_id}</p>
                    </div>

                    <div>
                        <p className="font-semibold">
                            Driver ID
                        </p>

                        <p>{ride.driver_id}</p>
                    </div>

                    <div>
                        <p className="font-semibold">
                            Available Seats
                        </p>

                        <p>
                            {ride.available_seats} /{" "}
                            {ride.total_seats}
                        </p>
                    </div>

                    <div>
                        <p className="font-semibold">
                            Price Per Seat
                        </p>

                        <p>
                            ₹{ride.price_per_seat}
                        </p>
                    </div>

                    <div>
                        <p className="font-semibold">
                            Status
                        </p>

                        <span className="bg-blue-100 text-blue-700 px-3 py-1 rounded-full">
                            {ride.status}
                        </span>
                    </div>

                </div>

                {ride.notes && (
                    <div className="mt-8">
                        <h2 className="text-xl font-semibold mb-2">
                            Notes
                        </h2>

                        <p className="text-gray-700">
                            {ride.notes}
                        </p>
                    </div>
                )}

                <div className="mt-8">
                    <button
                        onClick={handleBookRide}
                        disabled={
                            bookingLoading ||
                            ride.available_seats <= 0
                        }
                        className={`px-6 py-3 rounded-lg text-white font-medium ${
                            bookingLoading ||
                            ride.available_seats <= 0
                                ? "bg-gray-400 cursor-not-allowed"
                                : "bg-green-600 hover:bg-green-700"
                        }`}
                    >
                        {bookingLoading
                            ? "Booking..."
                            : ride.available_seats <= 0
                            ? "Ride Full"
                            : "Book Ride"}
                    </button>
                </div>

            </div>
        </Layout>
    );
}
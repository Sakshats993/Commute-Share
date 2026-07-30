import api from "./axios";

export async function bookRide(rideId) {
    const response = await api.post("/bookings", {
        ride_id: rideId,
    });

    return response.data;
}

export async function getMyBookings() {
    const response = await api.get("/bookings/me");
    return response.data;
}

export async function getRideBookings(rideId) {
    const response = await api.get(
        `/bookings/ride/${rideId}`
    );

    return response.data;
}

export async function getBookingStatistics() {
    const response = await api.get(
        "/bookings/me/statistics"
    );

    return response.data;
}

export async function cancelBooking(bookingId) {
    await api.delete(`/bookings/${bookingId}`);
}
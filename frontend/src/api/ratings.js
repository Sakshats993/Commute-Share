import api from "./axios";

export async function createRating(data) {
    const response = await api.post(
        "/ratings",
        data
    );

    return response.data;
}

export async function getUserRatings(userId) {
    const response = await api.get(
        `/ratings/user/${userId}`
    );

    return response.data;
}

export async function updateRating(
    ratingId,
    data
) {
    const response = await api.put(
        `/ratings/${ratingId}`,
        data
    );

    return response.data;
}

export async function deleteRating(ratingId) {
    await api.delete(
        `/ratings/${ratingId}`
    );
}
import api from "./axios";

export async function createRating(data) {
    const response = await api.post(
        "/ratings/",
        data
    );

    return response.data;
}

export async function getMyRatings() {
    const response = await api.get(
        "/ratings/me"
    );

    return response.data;
}

export async function getRatingCandidates() {
    const response = await api.get(
        "/ratings/candidates"
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
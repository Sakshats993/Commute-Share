export function getApiErrorMessage(error, fallback) {
    const detail = error?.response?.data?.detail;

    if (Array.isArray(detail)) {
        return detail.map((item) => item.msg).join(", ");
    }

    if (typeof detail === "string" && detail.trim()) {
        return detail;
    }

    return fallback;
}

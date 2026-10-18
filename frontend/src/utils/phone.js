/** Normalize an Indian mobile number to the ten digits required by the API. */
export function normalizeIndianMobileNumber(value) {
    const compact = value.trim().replace(/[\s-]/g, "");
    const national = compact.startsWith("+91")
        ? compact.slice(3)
        : compact.length === 12 && compact.startsWith("91")
            ? compact.slice(2)
            : compact;

    return /^[6-9]\d{9}$/.test(national) ? national : null;
}

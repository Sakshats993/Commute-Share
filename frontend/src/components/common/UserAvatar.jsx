import api from "../../api/axios";
import driverAvatar from "../../assets/avatars/driver.svg";
import passengerAvatar from "../../assets/avatars/passenger.svg";

export default function UserAvatar({ user, className = "", alt = "" }) {
    const role = String(user?.role ?? "").toLowerCase();
    const fallback = role === "driver" ? driverAvatar : passengerAvatar;
    const image = user?.profile_image;
    const source = image?.startsWith("/uploads/")
        ? `${api.defaults.baseURL}${image}`
        : image || fallback;

    return (
        <img
            src={source}
            alt={alt}
            className={className}
            onError={(event) => {
                event.currentTarget.onerror = null;
                event.currentTarget.src = fallback;
            }}
        />
    );
}

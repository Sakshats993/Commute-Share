import { useEffect } from "react";
import { MapContainer, Marker, Polyline, TileLayer, useMap } from "react-leaflet";
import L from "leaflet";
import markerIconImage from "leaflet/dist/images/marker-icon.png";
import markerIconRetinaImage from "leaflet/dist/images/marker-icon-2x.png";
import markerShadowImage from "leaflet/dist/images/marker-shadow.png";

const markerIcon = new L.Icon({
    iconUrl: markerIconImage,
    iconRetinaUrl: markerIconRetinaImage,
    shadowUrl: markerShadowImage,
    iconSize: [25, 41],
    iconAnchor: [12, 41],
});

function FitRoute({ points }) {
    const map = useMap();
    useEffect(() => {
        map.fitBounds(points, { padding: [28, 28] });
    }, [map, points]);
    return null;
}

function validPoint(latitude, longitude) {
    const lat = Number(latitude);
    const lon = Number(longitude);
    return Number.isFinite(lat) && Number.isFinite(lon) && Math.abs(lat) <= 90 && Math.abs(lon) <= 180
        ? [lat, lon]
        : null;
}

function straightLineKm(start, end) {
    const radians = (degrees) => degrees * Math.PI / 180;
    const [lat1, lon1] = start.map(radians);
    const [lat2, lon2] = end.map(radians);
    const a = Math.sin((lat2 - lat1) / 2) ** 2
        + Math.cos(lat1) * Math.cos(lat2) * Math.sin((lon2 - lon1) / 2) ** 2;
    return 6371 * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
}

export default function RideMap({ ride }) {
    const start = validPoint(ride?.pickup_latitude, ride?.pickup_longitude);
    const end = validPoint(ride?.destination_latitude, ride?.destination_longitude);
    if (!start || !end) {
        return <p className="rounded-xl border border-gray-200 bg-white p-4 text-sm text-gray-600">Map unavailable: valid pickup and destination coordinates were not provided.</p>;
    }
    const points = [start, end];

    return (
        <section aria-label="Ride route map" className="overflow-hidden rounded-2xl border border-gray-200 bg-white shadow-sm">
            <MapContainer bounds={points} scrollWheelZoom={false} className="h-72 w-full sm:h-96" aria-label="Map showing pickup and destination">
                <TileLayer
                    attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap contributors</a>'
                    url={import.meta.env.VITE_OSM_TILE_URL || "https://tile.openstreetmap.org/{z}/{x}/{y}.png"}
                />
                <FitRoute points={points} />
                <Marker position={start} icon={markerIcon} />
                <Marker position={end} icon={markerIcon} />
                <Polyline positions={points} pathOptions={{ color: "#2563eb", weight: 4, dashArray: "8 8" }} />
            </MapContainer>
            <p className="p-3 text-sm text-gray-600">Straight-line distance: {straightLineKm(start, end).toFixed(1)} km. This is not road distance or travel time.</p>
        </section>
    );
}

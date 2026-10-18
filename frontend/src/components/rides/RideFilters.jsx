import { Search, RotateCcw } from "lucide-react";
import { useState } from "react";

export default function RideFilters({ onSearch, loading = false }) {
    const emptyFilters = { source: "", destination: "", departure_date: "", minimum_available_seats: "", maximum_price: "", sort_by: "departure_time" };
    const [filters, setFilters] = useState(emptyFilters);

    function setField(name, value) {
        setFilters((current) => ({ ...current, [name]: value }));
    }

    function handleSubmit(e) {
        e.preventDefault();
        onSearch({
            ...filters,
            source: filters.source.trim(),
            destination: filters.destination.trim(),
            departure_date: filters.departure_date
                ? new Date(filters.departure_date).toISOString()
                : "",
        });
    }

    function handleReset() {
        setFilters(emptyFilters);
        onSearch(emptyFilters);
    }

    return (
        <form
            onSubmit={handleSubmit}
            className="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm"
        >
            <div className="mb-5">
                <h2 className="text-lg font-semibold text-gray-900">
                    Search Rides
                </h2>

                <p className="mt-1 text-sm text-gray-500">
                    Filter by route, departure, seats, fare, or sort order.
                </p>
            </div>

            <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
                <label className="block space-y-1 text-sm font-medium text-gray-700" htmlFor="ride-search-source">Pickup
                <input
                    id="ride-search-source"
                    type="text"
                    name="source"
                    placeholder="Pickup location"
                    value={filters.source}
                    onChange={(e) => setField("source", e.target.value)}
                    className="rounded-xl border border-gray-300 px-4 py-3 outline-none transition focus:border-blue-500 focus:ring-2 focus:ring-blue-200"
                />
                </label>

                <label className="block space-y-1 text-sm font-medium text-gray-700" htmlFor="ride-search-destination">Destination
                <input
                    id="ride-search-destination"
                    type="text"
                    name="destination"
                    placeholder="Destination"
                    value={filters.destination}
                    onChange={(e) => setField("destination", e.target.value)}
                    className="rounded-xl border border-gray-300 px-4 py-3 outline-none transition focus:border-blue-500 focus:ring-2 focus:ring-blue-200"
                />
                </label>

                <label className="block space-y-1 text-sm font-medium text-gray-700" htmlFor="ride-departure-after">Departure after
                    <input id="ride-departure-after" type="datetime-local" value={filters.departure_date} onChange={(e) => setField("departure_date", e.target.value)} className="w-full rounded-xl border border-gray-300 px-3 py-3 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-200" />
                </label>

                <label className="block space-y-1 text-sm font-medium text-gray-700" htmlFor="ride-min-seats">Minimum seats
                    <input id="ride-min-seats" type="number" min="1" max="99" inputMode="numeric" value={filters.minimum_available_seats} onChange={(e) => setField("minimum_available_seats", e.target.value)} placeholder="Any" className="w-full rounded-xl border border-gray-300 px-4 py-3 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-200" />
                </label>

                <label className="block space-y-1 text-sm font-medium text-gray-700" htmlFor="ride-maximum-fare">Maximum fare per seat (₹)
                    <input id="ride-maximum-fare" type="number" min="0" max="99999999.99" step="0.01" inputMode="decimal" value={filters.maximum_price} onChange={(e) => setField("maximum_price", e.target.value)} placeholder="Any" className="w-full rounded-xl border border-gray-300 px-4 py-3 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-200" />
                </label>

                <label className="block space-y-1 text-sm font-medium text-gray-700" htmlFor="ride-sort">Sort by
                    <select id="ride-sort" value={filters.sort_by} onChange={(e) => setField("sort_by", e.target.value)} className="w-full rounded-xl border border-gray-300 bg-white px-4 py-3 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-200">
                        <option value="departure_time">Departure time</option>
                        <option value="price">Price: lowest first</option>
                    </select>
                </label>

                <button
                    type="submit"
                    disabled={loading}
                    className="min-h-11 flex items-center justify-center gap-2 rounded-xl bg-blue-600 px-5 py-3 font-medium text-white transition hover:bg-blue-700 disabled:cursor-wait disabled:opacity-60"
                >
                    <Search size={18} />
                    Search
                </button>

                <button
                    type="button"
                    onClick={handleReset}
                    disabled={loading}
                    className="min-h-11 flex items-center justify-center gap-2 rounded-xl border border-gray-300 px-5 py-3 font-medium text-gray-700 transition hover:bg-gray-100 disabled:cursor-wait disabled:opacity-60"
                >
                    <RotateCcw size={18} />
                    Reset
                </button>
            </div>
        </form>
    );
}

import { Search, RotateCcw } from "lucide-react";
import { useState } from "react";

export default function RideFilters({ onSearch }) {
    const [source, setSource] = useState("");
    const [destination, setDestination] = useState("");

    function handleSubmit(e) {
        e.preventDefault();
        onSearch(source.trim(), destination.trim());
    }

    function handleReset() {
        setSource("");
        setDestination("");
        onSearch("", "");
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
                    Find rides by pickup location and destination.
                </p>
            </div>

            <div className="grid gap-4 lg:grid-cols-4">
                <input
                    type="text"
                    placeholder="Pickup location"
                    value={source}
                    onChange={(e) => setSource(e.target.value)}
                    className="rounded-xl border border-gray-300 px-4 py-3 outline-none transition focus:border-blue-500 focus:ring-2 focus:ring-blue-200"
                />

                <input
                    type="text"
                    placeholder="Destination"
                    value={destination}
                    onChange={(e) => setDestination(e.target.value)}
                    className="rounded-xl border border-gray-300 px-4 py-3 outline-none transition focus:border-blue-500 focus:ring-2 focus:ring-blue-200"
                />

                <button
                    type="submit"
                    className="flex items-center justify-center gap-2 rounded-xl bg-blue-600 px-5 py-3 font-medium text-white transition hover:bg-blue-700"
                >
                    <Search size={18} />
                    Search
                </button>

                <button
                    type="button"
                    onClick={handleReset}
                    className="flex items-center justify-center gap-2 rounded-xl border border-gray-300 px-5 py-3 font-medium text-gray-700 transition hover:bg-gray-100"
                >
                    <RotateCcw size={18} />
                    Reset
                </button>
            </div>
        </form>
    );
}
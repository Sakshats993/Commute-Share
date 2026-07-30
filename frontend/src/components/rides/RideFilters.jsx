import { useState } from "react";

export default function RideFilters({ onSearch }) {
    const [source, setSource] = useState("");
    const [destination, setDestination] = useState("");

    function handleSubmit(e) {
        e.preventDefault();
        onSearch(source, destination);
    }

    return (
        <form
            onSubmit={handleSubmit}
            className="bg-white rounded-xl shadow p-6 mb-6"
        >
            <div className="grid md:grid-cols-3 gap-4">
                <input
                    className="border rounded-lg p-3"
                    placeholder="Pickup Location"
                    value={source}
                    onChange={(e) =>
                        setSource(e.target.value)
                    }
                />

                <input
                    className="border rounded-lg p-3"
                    placeholder="Destination"
                    value={destination}
                    onChange={(e) =>
                        setDestination(e.target.value)
                    }
                />

                <button
                    className="bg-blue-600 text-white rounded-lg"
                >
                    Search
                </button>
            </div>
        </form>
    );
}
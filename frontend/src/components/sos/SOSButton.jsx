import { AlertTriangle } from "lucide-react";

export default function SOSButton({
    onTrigger,
    loading,
}) {
    return (
        <button
            onClick={onTrigger}
            disabled={loading}
            className="w-full bg-red-600 hover:bg-red-700 disabled:bg-red-400 text-white rounded-xl py-5 flex items-center justify-center gap-3 text-lg font-semibold shadow-lg transition"
        >
            <AlertTriangle size={26} />

            {loading
                ? "Triggering SOS..."
                : "Trigger SOS"}
        </button>
    );
}
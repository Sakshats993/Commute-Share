export default function SafetyTriage({ events, onUpdate }) {
    return (
        <section className="space-y-4" aria-labelledby="safety-triage-title">
            <div>
                <h2 id="safety-triage-title" className="text-2xl font-semibold text-gray-900">SOS safety triage</h2>
                <p className="mt-1 text-sm text-gray-600">These events are recorded in CommuteShare. This dashboard does not contact emergency services.</p>
            </div>
            {events.length === 0 ? (
                <p className="rounded-xl border border-gray-200 bg-white p-5 text-gray-600">No SOS events have been recorded.</p>
            ) : events.map((event) => (
                <article key={event.id} className="space-y-3 rounded-xl border border-gray-200 bg-white p-4 sm:p-5">
                    <div className="flex flex-col justify-between gap-2 sm:flex-row sm:items-start">
                        <div>
                            <h3 className="font-semibold text-gray-900">Safety event #{event.id}: {event.status}</h3>
                            <p className="mt-1 text-sm text-gray-600">User #{event.user_id} · Ride {event.ride_id ?? "not associated"} · {new Date(event.created_at).toLocaleString()}</p>
                            {event.description && <p className="mt-2 break-words text-sm text-gray-700">{event.description}</p>}
                            {event.latitude != null && event.longitude != null && <p className="mt-1 text-sm text-gray-600">Location: {event.latitude}, {event.longitude}</p>}
                        </div>
                        <div className="flex flex-wrap gap-2">
                            {event.status === "active" && <button type="button" onClick={() => onUpdate(event.id, "acknowledge")} className="min-h-11 rounded-lg bg-amber-600 px-4 py-2 font-medium text-white hover:bg-amber-700">Acknowledge</button>}
                            {event.status !== "resolved" && <button type="button" onClick={() => onUpdate(event.id, "resolve")} className="min-h-11 rounded-lg bg-green-700 px-4 py-2 font-medium text-white hover:bg-green-800">Resolve</button>}
                        </div>
                    </div>
                </article>
            ))}
        </section>
    );
}

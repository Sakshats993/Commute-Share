    import { useState } from "react";

    import * as sosApi from "../api/sos";

    export default function useSOS() {
        const [events, setEvents] = useState([]);

        const [loading, setLoading] =
            useState(false);

        async function loadEvents() {
            try {
                setLoading(true);

                const data =
                    await sosApi.getMySOSEvents();

                setEvents(data);
            } finally {
                setLoading(false);
            }
        }

        async function trigger(data) {
            const event =
                await sosApi.triggerSOS(data);

            setEvents((prev) => [
                event,
                ...prev,
            ]);

            return event;
        }

        async function getDetails(id) {
            return sosApi.getSOSDetails(id);
        }

        return {
            events,
            loading,
            loadEvents,
            trigger,
            getDetails,
        };
    }
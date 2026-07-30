import { useEffect, useState } from "react";
import toast from "react-hot-toast";

import Layout from "../components/ui/Layout";
import LoadingSpinner from "../components/ui/LoadingSpinner";
import EmptyState from "../components/ui/EmptyState";

import SOSButton from "../components/sos/SOSButton";
import SOSHistory from "../components/sos/SOSHistory";

import useSOS from "../hooks/useSOS";

export default function SOSPage() {
    const {
        events,
        loading,
        loadEvents,
        trigger,
        getDetails,
    } = useSOS();

    const [triggering, setTriggering] =
        useState(false);

    useEffect(() => {
        loadEvents();
    }, []);

    async function handleTrigger() {
        const ride_id = prompt("Ride ID");

        if (!ride_id) return;

        const emergency_type = prompt(
            "Emergency Type"
        );

        if (!emergency_type) return;

        const description =
            prompt("Description") || "";

        const latitude = Number(
            prompt("Latitude")
        );

        const longitude = Number(
            prompt("Longitude")
        );

        try {
            setTriggering(true);

            await trigger({
                ride_id: Number(ride_id),
                emergency_type,
                description,
                latitude,
                longitude,
            });

            toast.success(
                "SOS triggered successfully."
            );
        } catch (error) {
            toast.error(
                error.response?.data?.detail ??
                    "Unable to trigger SOS."
            );
        } finally {
            setTriggering(false);
        }
    }

    async function handleView(id) {
        try {
            const sos =
                await getDetails(id);

            toast.success(
                `Status: ${sos.status}`
            );
        } catch {
            toast.error(
                "Unable to load SOS details."
            );
        }
    }

    if (loading) {
        return (
            <Layout>
                <LoadingSpinner />
            </Layout>
        );
    }

    return (
        <Layout>
            <div className="space-y-6">
                <h1 className="text-3xl font-bold">
                    Emergency SOS
                </h1>

                <SOSButton
                    onTrigger={handleTrigger}
                    loading={triggering}
                />

                {events.length === 0 ? (
                    <EmptyState
                        title="No SOS Events"
                        description="You haven't triggered any emergency events."
                    />
                ) : (
                    <SOSHistory
                        events={events}
                        onView={handleView}
                    />
                )}
            </div>
        </Layout>
    );
}
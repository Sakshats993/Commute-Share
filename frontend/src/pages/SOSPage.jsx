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
        try {
            setTriggering(true);

            const triggerSOS = async (
                latitude = null,
                longitude = null
            ) => {
                await trigger({
                    emergency_type: "Emergency",
                    description:
                        "SOS triggered by user.",
                    latitude,
                    longitude,
                });
            };

            // Try to get the user's current location
            if ("geolocation" in navigator) {
                navigator.geolocation.getCurrentPosition(
                    async (position) => {
                        try {
                            await triggerSOS(
                                position.coords.latitude,
                                position.coords.longitude
                            );

                            toast.success("SOS event recorded. Admins are notified in-app when configured.");

                            await loadEvents();
                        } catch (error) {
                            toast.error(
                                error.response?.data?.detail ??
                                    "Unable to trigger SOS."
                            );
                        } finally {
                            setTriggering(false);
                        }
                    },
                    async () => {
                        // Location unavailable/denied.
                        // SOS should still work.
                        try {
                            await triggerSOS();

                            toast.success("SOS event recorded without location. Admins are notified in-app when configured.");

                            await loadEvents();
                        } catch (error) {
                            toast.error(
                                error.response?.data?.detail ??
                                    "Unable to trigger SOS."
                            );
                        } finally {
                            setTriggering(false);
                        }
                    },
                    {
                        enableHighAccuracy: true,
                        timeout: 10000,
                        maximumAge: 0,
                    }
                );
            } else {
                await triggerSOS();

                toast.success("SOS event recorded without location. Admins are notified in-app when configured.");

                await loadEvents();

                setTriggering(false);
            }
        } catch (error) {
            toast.error(
                error.response?.data?.detail ??
                    "Unable to trigger SOS."
            );

            setTriggering(false);
        }
    }

    async function handleView(id) {
        try {
            const sos = await getDetails(id);

            toast.success(
                `SOS Status: ${sos.status}`
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
                <div className="flex justify-center py-24">
                    <LoadingSpinner />
                </div>
            </Layout>
        );
    }

    return (
        <Layout>
            <div className="space-y-6">

                <div>
                    <h1 className="text-3xl font-bold text-gray-900">
                        Emergency SOS
                    </h1>

                    <p className="mt-2 text-gray-500">
                        Record a safety event during an active ride. It appears in CommuteShare and notifies configured administrators in-app. This does not contact emergency services or provide live dispatch; call local emergency services if you need immediate help. Location is shared only if you allow browser location access.
                    </p>
                </div>

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

import { useState } from "react";
import { useNavigate } from "react-router-dom";
import toast from "react-hot-toast";

import Layout from "../components/ui/Layout";
import LoadingSpinner from "../components/ui/LoadingSpinner";
import EmptyState from "../components/ui/EmptyState";

import RideList from "../components/rides/RideList";
import RideForm from "../components/rides/RideForm";
import RideFilters from "../components/rides/RideFilters";
import DeleteRideModal from "../components/rides/DeleteRideModal";

import useAuth from "../hooks/useAuth";
import useRides from "../hooks/useRides";

export default function RidesPage() {
    const navigate = useNavigate();

    const { user } = useAuth();

    const {
        rides,
        loading,
        search,
        addRide,
        editRide,
        removeRide,
    } = useRides();

    const [editingRide, setEditingRide] = useState(null);
    const [deletingRide, setDeletingRide] = useState(null);
    const [showForm, setShowForm] = useState(false);

    const isDriver = user?.role === "driver";

    async function handleCreate(data) {
        try {
            await addRide(data);
            toast.success("Ride created successfully");
            setShowForm(false);
        } catch {
            toast.error("Failed to create ride");
        }
    }

    async function handleUpdate(data) {
        try {
            await editRide(editingRide.id, data);
            toast.success("Ride updated successfully");
            setEditingRide(null);
        } catch {
            toast.error("Failed to update ride");
        }
    }

    async function handleDelete(id) {
        try {
            await removeRide(id);
            toast.success("Ride deleted successfully");
            setDeletingRide(null);
        } catch {
            toast.error("Failed to delete ride");
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
            <div className="mb-8 flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
                <div>
                    <h1 className="text-4xl font-bold text-gray-900">
                        Available Rides
                    </h1>

                    <p className="mt-2 text-gray-500">
                        Browse available rides and manage your trips.
                    </p>
                </div>

                {isDriver && (
                    <button
                        onClick={() => setShowForm(true)}
                        className="rounded-xl bg-blue-600 px-6 py-3 font-medium text-white transition hover:bg-blue-700"
                    >
                        + Create Ride
                    </button>
                )}
            </div>

            <div className="mb-6 rounded-2xl border bg-white p-5 shadow-sm">
                <RideFilters onSearch={search} />
            </div>

            {isDriver && (showForm || editingRide) && (
                <div className="mb-6 rounded-2xl border bg-white p-6 shadow-sm">
                    <RideForm
                        initialData={editingRide}
                        onSubmit={editingRide ? handleUpdate : handleCreate}
                        onCancel={() => {
                            setEditingRide(null);
                            setShowForm(false);
                        }}
                    />
                </div>
            )}

            {rides.length === 0 ? (
                <EmptyState
                    title="No rides available"
                    description="No rides match your search. Drivers can create a new ride."
                />
            ) : (
                <RideList
                    rides={rides}
                    onView={(ride) => navigate(`/rides/${ride.id}`)}
                    onEdit={setEditingRide}
                    onDelete={setDeletingRide}
                />
            )}

            <DeleteRideModal
                ride={deletingRide}
                onConfirm={handleDelete}
                onCancel={() => setDeletingRide(null)}
            />
        </Layout>
    );
}
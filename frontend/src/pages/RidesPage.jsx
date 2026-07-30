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

import useRides from "../hooks/useRides";

export default function RidesPage() {
    const navigate = useNavigate();

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
            toast.success("Ride updated");
            setEditingRide(null);
        } catch {
            toast.error("Failed to update ride");
        }
    }

    async function handleDelete(id) {
        try {
            await removeRide(id);
            toast.success("Ride deleted");
            setDeletingRide(null);
        } catch {
            toast.error("Failed to delete ride");
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
            <div className="flex justify-between items-center mb-6">
                <h1 className="text-3xl font-bold">
                    Available Rides
                </h1>

                <button
                    onClick={() => setShowForm(true)}
                    className="bg-blue-600 text-white px-5 py-2 rounded-lg"
                >
                    Create Ride
                </button>
            </div>

            <RideFilters onSearch={search} />

            {(showForm || editingRide) && (
                <div className="bg-white shadow rounded-xl p-6 mb-6">
                    <RideForm
                        initialData={editingRide}
                        onSubmit={
                            editingRide
                                ? handleUpdate
                                : handleCreate
                        }
                        onCancel={() => {
                            setShowForm(false);
                            setEditingRide(null);
                        }}
                    />
                </div>
            )}

            {rides.length === 0 ? (
                <EmptyState
                    title="No rides found"
                    description="Create a ride or search another route."
                />
            ) : (
                <RideList
                    rides={rides}
                    onView={(ride) =>
                        navigate(`/rides/${ride.id}`)
                    }
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
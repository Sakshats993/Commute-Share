import { useState } from "react";
import toast from "react-hot-toast";

import Layout from "../components/ui/Layout";
import EmptyState from "../components/ui/EmptyState";
import LoadingSpinner from "../components/ui/LoadingSpinner";
import ErrorMessage from "../components/ui/ErrorMessage";

import VehicleForm from "../components/vehicles/VehicleForm";
import VehicleList from "../components/vehicles/VehicleList";
import DeleteVehicleModal from "../components/vehicles/DeleteVehicleModal";

import useVehicles from "../hooks/useVehicles";
import { getApiErrorMessage } from "../utils/apiError";

export default function VehiclesPage() {
    const {
        vehicles,
        loading,
        error,
        loadVehicles,
        addVehicle,
        editVehicle,
        removeVehicle,
    } = useVehicles();

    const [editing, setEditing] = useState(null);
    const [deleting, setDeleting] = useState(null);
    const [showForm, setShowForm] = useState(false);

    async function handleCreate(data) {
        try {
            await addVehicle(data);
            toast.success("Vehicle added successfully");
            setShowForm(false);
        } catch (error) {
            toast.error(getApiErrorMessage(error, "Failed to add vehicle."));
        }
    }

    async function handleUpdate(data) {
        try {
            await editVehicle(editing.id, data);
            toast.success("Vehicle updated successfully");
            setEditing(null);
        } catch (error) {
            toast.error(getApiErrorMessage(error, "Failed to update vehicle."));
        }
    }

    async function handleDelete(id) {
        try {
            await removeVehicle(id);
            toast.success("Vehicle deleted successfully");
            setDeleting(null);
        } catch (error) {
            toast.error(getApiErrorMessage(error, "Failed to delete vehicle."));
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
                    <h1 className="text-2xl font-bold text-gray-900 sm:text-3xl lg:text-4xl">
                        My Vehicles
                    </h1>

                    <p className="mt-2 text-gray-500">
                        Register and manage the vehicles you use for ride sharing.
                    </p>
                </div>

                <button
                    onClick={() => setShowForm(true)}
                    className="rounded-xl bg-blue-600 px-6 py-3 font-medium text-white transition hover:bg-blue-700"
                >
                    + Add Vehicle
                </button>
            </div>

            {(showForm || editing) && (
                <div className="mb-8 rounded-2xl border border-gray-200 bg-white p-6 shadow-sm">
                    <VehicleForm
                        initialData={editing}
                        onSubmit={editing ? handleUpdate : handleCreate}
                        onCancel={() => {
                            setEditing(null);
                            setShowForm(false);
                        }}
                    />
                </div>
            )}

            {error ? (
                <ErrorMessage
                    message={getApiErrorMessage(error, "Unable to load vehicles right now.")}
                    onRetry={loadVehicles}
                />
            ) : vehicles.length === 0 ? (
                <EmptyState
                    title="No Vehicles Registered"
                    description="Add your first vehicle to start creating rides."
                />
            ) : (
                <VehicleList
                    vehicles={vehicles}
                    onEdit={setEditing}
                    onDelete={setDeleting}
                />
            )}

            <DeleteVehicleModal
                vehicle={deleting}
                onConfirm={handleDelete}
                onCancel={() => setDeleting(null)}
            />
        </Layout>
    );
}

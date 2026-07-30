import { useState } from "react";
import toast from "react-hot-toast";

import Layout from "../components/ui/Layout";
import EmptyState from "../components/ui/EmptyState";
import LoadingSpinner from "../components/ui/LoadingSpinner";

import VehicleForm from "../components/vehicles/VehicleForm";
import VehicleList from "../components/vehicles/VehicleList";
import DeleteVehicleModal from "../components/vehicles/DeleteVehicleModal";

import useVehicles from "../hooks/useVehicles";

export default function VehiclesPage() {
    const {
        vehicles,
        loading,
        addVehicle,
        editVehicle,
        removeVehicle,
    } = useVehicles();

    const [editing, setEditing] =
        useState(null);

    const [deleting, setDeleting] =
        useState(null);

    const [showForm, setShowForm] =
        useState(false);

    async function handleCreate(data) {
        await addVehicle(data);

        toast.success("Vehicle added");

        setShowForm(false);
    }

    async function handleUpdate(data) {
        await editVehicle(editing.id, data);

        toast.success("Vehicle updated");

        setEditing(null);
    }

    async function handleDelete(id) {
        await removeVehicle(id);

        toast.success("Vehicle deleted");

        setDeleting(null);
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
            <div className="flex justify-between items-center mb-8">
                <h1 className="text-3xl font-bold">
                    My Vehicles
                </h1>

                <button
                    onClick={() =>
                        setShowForm(true)
                    }
                    className="bg-blue-600 text-white px-5 py-3 rounded-lg"
                >
                    Add Vehicle
                </button>
            </div>

            {(showForm || editing) && (
                <div className="bg-white rounded-xl shadow p-6 mb-8">
                    <VehicleForm
                        initialData={editing}
                        onSubmit={
                            editing
                                ? handleUpdate
                                : handleCreate
                        }
                        onCancel={() => {
                            setEditing(null);
                            setShowForm(false);
                        }}
                    />
                </div>
            )}

            {vehicles.length === 0 ? (
                <EmptyState
                    title="No Vehicles"
                    description="Register your first vehicle."
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
                onCancel={() =>
                    setDeleting(null)
                }
            />
        </Layout>
    );
}
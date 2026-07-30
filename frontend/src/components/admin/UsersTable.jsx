export default function UsersTable({
    users,
    onActivate,
    onDeactivate,
}) {
    return (
        <div className="bg-white rounded-xl shadow border overflow-x-auto">

            <table className="min-w-full">

                <thead className="bg-gray-100">

                    <tr>
                        <th className="text-left p-4">ID</th>
                        <th className="text-left p-4">Name</th>
                        <th className="text-left p-4">Email</th>
                        <th className="text-left p-4">Status</th>
                        <th className="text-left p-4">Action</th>
                    </tr>

                </thead>

                <tbody>

                    {users.map((user) => (
                        <tr
                            key={user.id}
                            className="border-t"
                        >
                            <td className="p-4">
                                {user.id}
                            </td>

                            <td className="p-4">
                                {user.full_name}
                            </td>

                            <td className="p-4">
                                {user.email}
                            </td>

                            <td className="p-4">
                                {user.is_active
                                    ? "Active"
                                    : "Inactive"}
                            </td>

                            <td className="p-4">

                                {user.is_active ? (
                                    <button
                                        onClick={() =>
                                            onDeactivate(
                                                user.id
                                            )
                                        }
                                        className="bg-red-600 text-white px-3 py-2 rounded-lg"
                                    >
                                        Deactivate
                                    </button>
                                ) : (
                                    <button
                                        onClick={() =>
                                            onActivate(
                                                user.id
                                            )
                                        }
                                        className="bg-green-600 text-white px-3 py-2 rounded-lg"
                                    >
                                        Activate
                                    </button>
                                )}

                            </td>

                        </tr>
                    ))}

                </tbody>

            </table>

        </div>
    );
}
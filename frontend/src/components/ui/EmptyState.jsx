export default function EmptyState({
    title,
    description,
}) {
    return (
        <section aria-labelledby="empty-state-title" className="rounded-xl bg-white p-6 text-center shadow sm:p-10">
            <h2 id="empty-state-title" className="mb-2 text-xl font-semibold">
                {title}
            </h2>

            <p className="text-gray-500">
                {description}
            </p>
        </section>
    );
}

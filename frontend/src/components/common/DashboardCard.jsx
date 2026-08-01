export default function DashboardCard({
    title,
    value,
    description,
    onClick,
}) {
    const clickable = typeof onClick === "function";

    return (
        <div
            onClick={onClick}
            onKeyDown={(e) => {
                if (
                    clickable &&
                    (e.key === "Enter" || e.key === " ")
                ) {
                    e.preventDefault();
                    onClick();
                }
            }}
            role={clickable ? "button" : undefined}
            tabIndex={clickable ? 0 : undefined}
            className={`
                rounded-2xl
                border
                border-gray-200
                bg-white
                p-6
                shadow-sm
                transition-all
                duration-200
                ${
                    clickable
                        ? "cursor-pointer hover:-translate-y-1 hover:shadow-xl active:scale-[0.98] focus:outline-none focus:ring-2 focus:ring-green-500"
                        : ""
                }
            `}
        >
            <div className="flex items-start justify-between">
                <div>
                    <p className="text-sm font-medium uppercase tracking-wide text-gray-500">
                        {title}
                    </p>

                    <h2 className="mt-3 text-4xl font-bold text-gray-900">
                        {value}
                    </h2>

                    {description && (
                        <p className="mt-3 text-sm text-gray-500">
                            {description}
                        </p>
                    )}
                </div>

                <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-green-100">
                    <div className="h-3 w-3 rounded-full bg-green-600"></div>
                </div>
            </div>
        </div>
    );
}
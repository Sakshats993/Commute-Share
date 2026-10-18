export default function ErrorMessage({
    message = "Something went wrong. Please try again.",
    onRetry,
}) {
    return (
        <div role="alert" className="flex flex-col gap-3 rounded-xl border border-red-200 bg-red-50 p-4 text-red-800 sm:flex-row sm:items-center sm:justify-between">
            <p>{message}</p>
            {onRetry && (
                <button
                    type="button"
                    onClick={onRetry}
                    className="w-fit rounded-lg border border-red-300 px-4 py-2 font-medium text-red-800 hover:bg-red-100 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-red-700"
                >
                    Try again
                </button>
            )}
        </div>
    );
}

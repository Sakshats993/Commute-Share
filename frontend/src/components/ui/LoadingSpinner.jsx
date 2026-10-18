export default function LoadingSpinner({
    text = "Loading...",
}) {
    return (
        <div role="status" aria-live="polite" className="flex items-center justify-center py-12">
            <div className="text-center">
                <div aria-hidden="true" className="mx-auto h-10 w-10 animate-spin rounded-full border-b-2 border-blue-600 motion-reduce:animate-none"></div>

                <p className="mt-4 text-gray-600">
                    {text}
                </p>
            </div>
        </div>
    );
}

export default function LoadingSpinner({
    text = "Loading...",
}) {
    return (
        <div className="flex items-center justify-center py-12">
            <div className="text-center">
                <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-blue-600 mx-auto"></div>

                <p className="mt-4 text-gray-600">
                    {text}
                </p>
            </div>
        </div>
    );
}
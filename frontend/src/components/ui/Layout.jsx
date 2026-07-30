import Navbar from "../layout/Navbar";
import Sidebar from "../layout/Sidebar";

export default function Layout({
    children,
}) {
    return (
        <div className="flex bg-slate-100 min-h-screen">
            <Sidebar />

            <div className="flex-1 flex flex-col">
                <Navbar />

                <main className="flex-1 p-8 overflow-auto">
                    {children}
                </main>
            </div>
        </div>
    );
}
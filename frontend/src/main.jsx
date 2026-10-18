import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import { Toaster } from "react-hot-toast";

import App from "./App";
import "./index.css";
import "leaflet/dist/leaflet.css";

import { AuthProvider } from "./context/AuthContext";

try {
    const savedTheme = localStorage.getItem("commuteshare-theme");
    document.documentElement.classList.toggle("dark", savedTheme === "dark");
} catch {
    document.documentElement.classList.remove("dark");
}

ReactDOM.createRoot(
    document.getElementById("root")
).render(
    <React.StrictMode>
        <BrowserRouter>
            <AuthProvider>
                <Toaster />

                <App />
            </AuthProvider>
        </BrowserRouter>
    </React.StrictMode>
);

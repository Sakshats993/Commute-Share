import { useState } from "react";
import { Moon, Sun } from "lucide-react";

export default function ThemeToggle() {
    const [darkMode, setDarkMode] = useState(() => document.documentElement.classList.contains("dark"));

    function toggleTheme() {
        const next = !darkMode;
        document.documentElement.classList.toggle("dark", next);
        try {
            localStorage.setItem("commuteshare-theme", next ? "dark" : "light");
        } catch {
            // The selected theme still applies for this page if storage is unavailable.
        }
        setDarkMode(next);
    }

    return (
        <button
            type="button"
            onClick={toggleTheme}
            aria-label={`Switch to ${darkMode ? "light" : "dark"} mode`}
            aria-pressed={darkMode}
            className="fixed right-4 top-4 z-10 rounded-lg bg-white p-2 text-slate-700 shadow hover:bg-slate-100 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-600 dark:bg-slate-800 dark:text-slate-100 dark:hover:bg-slate-700"
        >
            {darkMode ? <Sun size={20} aria-hidden="true" /> : <Moon size={20} aria-hidden="true" />}
        </button>
    );
}

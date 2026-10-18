import logo from "../../assets/images/logo.png";

export default function AuthBrand({ variant = "stacked" }) {
    if (variant === "navbar") {
        return (
            <span className="flex min-w-0 items-center gap-2 sm:gap-2.5">
                <img src={logo} alt="" className="h-10 w-10 shrink-0 rounded-lg object-contain" />
                <span className="hidden whitespace-nowrap text-base font-extrabold tracking-tight text-slate-900 dark:text-white sm:inline">
                    Commute<span className="text-green-700 dark:text-green-400">Share</span>
                </span>
            </span>
        );
    }

    if (variant === "horizontal") {
        return (
            <div className="inline-flex items-center gap-2.5">
                <img src={logo} alt="" className="h-12 w-12 shrink-0 rounded-xl object-contain" />
                <span className="text-xl font-extrabold tracking-tight text-slate-900 dark:text-white">
                    Commute<span className="text-green-700 dark:text-green-400">Share</span>
                </span>
            </div>
        );
    }

    return (
        <div className="mb-5 flex flex-col items-center">
            <img src={logo} alt="" className="h-14 w-14 rounded-xl object-contain" />
            <span className="mt-2 text-sm font-extrabold tracking-tight text-slate-800 dark:text-white">
                Commute<span className="text-green-700 dark:text-green-400">Share</span>
            </span>
        </div>
    );
}

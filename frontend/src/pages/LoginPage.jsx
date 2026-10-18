import LoginForm from "../components/auth/LoginForm";
import AuthPageShell from "../components/auth/AuthPageShell";

export default function LoginPage() {
    return (
        <AuthPageShell className="max-w-md" showTopBrand>
            <LoginForm />
        </AuthPageShell>
    );
}

// src/App.tsx
import { useEffect, useState } from "react";
import { LoginForm } from "./components/auth/LoginForm";
import { SignUpForm } from "./components/auth/SignUpForm";
import { TodoList } from "./components/todo/TodoList";
import { api } from "./api/api";
import { loadCsrfToken } from "./api/csrf";

type AuthMode = "login" | "register";

function App() {
  const [loggedIn, setLoggedIn] = useState(false);
  const [authMode, setAuthMode] = useState<AuthMode>("login");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api
      .get("/api/me")
      .then(() => setLoggedIn(true))
      .catch(() => setLoggedIn(false))
      .finally(() => setLoading(false));
      loadCsrfToken().catch(console.error);
  }, []);

  if (loading) return <p style={{ textAlign: "center" }}>Loading...</p>;

  if (loggedIn) {
    return <TodoList onLogout={() => setLoggedIn(false)} />;
  }

  if (authMode === "login") {
    return (
      <LoginForm
        onSuccess={() => setLoggedIn(true)}
        onChangeMode={() => setAuthMode("register")}
      />
    );
  }

  return (
    <SignUpForm
      onSuccess={() => setAuthMode("login")}
      onChangeMode={() => setAuthMode("login")}
    />
  );
}

export default App;

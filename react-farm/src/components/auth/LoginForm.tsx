// src/components/auth/LoginForm.tsx
import { useState } from "react";
import type { User } from "../../types/auth";
import { AuthApi } from "../../api/api";
import { LoginFormView } from "./LoginFormView";

interface LoginFormProps {
  onSuccess: () => void;
  onChangeMode: (mode: "register") => void;
}

export function LoginForm({ onSuccess, onChangeMode }: LoginFormProps) {
  const [form, setForm] = useState<User>({ email: "", password: "" });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      const csrf = await AuthApi.getCsrfToken();
      await AuthApi.login(form, csrf);
      onSuccess();
    } catch (err) {
      console.error(err);
      setError("メールアドレスまたはパスワードが正しくありません。");
    } finally {
      setLoading(false);
    }
  };

  return (
    <LoginFormView
      form={form}
      loading={loading}
      error={error}
      onSubmit={handleSubmit}
      onChange={handleChange}
      onChangeMode={onChangeMode}
    />
  );
}

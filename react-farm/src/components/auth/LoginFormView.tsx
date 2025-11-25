// src/components/auth/LoginFormView.tsx
import type { User } from "../../types/auth";
import "./LoginForm.css";

interface LoginFormViewProps {
  form: User;
  loading: boolean;
  error: string | null;
  onSubmit: (e: React.FormEvent) => void;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  onChangeMode: (mode: "register") => void;
}

export function LoginFormView({
  form,
  loading,
  error,
  onSubmit,
  onChange,
  onChangeMode,
}: LoginFormViewProps) {
  return (
    <div className="login-wrapper">
      <div className="login-card">
        <h1 className="login-title">Todo App</h1>
        <p className="login-subtitle">ログインしてタスクを管理しましょう</p>

        <form className="login-form" onSubmit={onSubmit}>
          {/* 이메일 */}
          <div className="login-field">
            <label htmlFor="email" className="login-label">
              メールアドレス
            </label>
            <input
              id="email"
              name="email"
              type="email"
              className="login-input"
              value={form.email}
              onChange={onChange}
              required
            />
          </div>

          {/* 비밀번호 */}
          <div className="login-field">
            <label htmlFor="password" className="login-label">
              パスワード
            </label>
            <input
              id="password"
              name="password"
              type="password"
              className="login-input"
              value={form.password}
              onChange={onChange}
              required
            />
          </div>

          {error && <div className="login-error">{error}</div>}

          <button
            type="submit"
            className="login-button"
            disabled={loading}
          >
            {loading ? "ログイン中..." : "ログイン"}
          </button>
        </form>

        <p className="login-hint">
          アカウントをお持ちでない方は
          <button
            type="button"
            className="link-button"
            onClick={() => onChangeMode("register")}
          >
            新規登録
          </button>
        </p>
      </div>
    </div>
  );
}

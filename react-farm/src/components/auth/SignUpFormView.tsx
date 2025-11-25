// src/components/auth/SignUpFormView.tsx
import type { User } from "../../types/auth";
import "./LoginForm.css";

interface SignUpFormViewProps {
  form: User;
  passwordConfirm: string;
  loading: boolean;
  error: string | null;
  onSubmit: (e: React.FormEvent) => void;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  onChangeMode: (mode: "login") => void;
}

export function SignUpFormView({
  form,
  passwordConfirm,
  loading,
  error,
  onSubmit,
  onChange,
  onChangeMode,
}: SignUpFormViewProps) {
  return (
    <div className="login-wrapper">
      <div className="login-card">
        <h1 className="login-title">アカウント登録</h1>
        <p className="login-subtitle">メールアドレスとパスワードで新規登録</p>

        <form className="login-form" onSubmit={onSubmit}>
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

          <div className="login-field">
            <label htmlFor="passwordConfirm" className="login-label">
              パスワード（確認）
            </label>
            <input
              id="passwordConfirm"
              name="passwordConfirm"
              type="password"
              className="login-input"
              value={passwordConfirm}
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
            {loading ? "登録中..." : "登録する"}
          </button>
        </form>

        <p className="login-hint">
          すでにアカウントをお持ちの方は{" "}
          <button
            type="button"
            className="link-button"
            onClick={() => onChangeMode("login")}
          >
            ログインはこちら
          </button>
        </p>
      </div>
    </div>
  );
}

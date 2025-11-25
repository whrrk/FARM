// src/components/auth/SignUpForm.tsx
import { useState } from "react";
import type { User } from "../../types/auth";
import { AuthApi } from "../../api/api";
import { SignUpFormView } from "./SignUpFormView";

interface SignUpFormProps {
  onSuccess: () => void;                  // 회원가입 후 로그인 화면으로 이동
  onChangeMode: (mode: "login") => void;  // "이미 계정 있음 → 로그인"
}

export function SignUpForm({ onSuccess, onChangeMode }: SignUpFormProps) {
  const [form, setForm] = useState<User>({
    email: "",
    password: "",
  });
  const [passwordConfirm, setPasswordConfirm] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    if (name === "passwordConfirm") {
      setPasswordConfirm(value);
    } else {
      setForm((prev) => ({ ...prev, [name]: value }));
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (form.password !== passwordConfirm) {
      setError("パスワードが一致しません。");
      return;
    }

    setLoading(true);
    try {
      const csrf = await AuthApi.getCsrfToken();
      await AuthApi.signup(form, csrf);
      // 회원가입 성공 → 로그인 화면으로 보내기
      onSuccess();
    } catch (err) {
      console.error(err);
      setError("ユーザー登録に失敗しました。");
    } finally {
      setLoading(false);
    }
  };

  return (
    <SignUpFormView
      form={form}
      passwordConfirm={passwordConfirm}
      loading={loading}
      error={error}
      onSubmit={handleSubmit}
      onChange={handleChange}
      onChangeMode={onChangeMode}
    />
  );
}

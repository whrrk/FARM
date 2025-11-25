// src/api/authApi.ts
import axios from "axios";
import type { CsrfToken } from "../types/index";
import type { UserInfo, User } from "../types/auth";
import { type Todo, type CreateTodo } from "../types/todo";

export const api = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL,
    withCredentials: true, // 쿠키 쓰면 true로
  });

export const AuthApi = {
  getCsrfToken: async (): Promise<string> => {
    const res = await api.get<CsrfToken>("/api/csrf-token");
    return res.data.csrf_token;
  },

  signup: async (data: User, csrfToken: string): Promise<UserInfo> => {
    const res = await api.post<UserInfo>("/api/signup", data, {
      headers: { "X-CSRF-Token": csrfToken },
    });
    return res.data;
  },

  login: async (data: User, csrfToken: string): Promise<void> => {
    await api.post("/api/login", data, {
      headers: { "X-CSRF-Token": csrfToken },
    });
    // JWT는 httpOnly 쿠키에 들어가니까 따로 리턴값 안 써도 됨
  },

  logout: async (): Promise<void> => {
    await api.post("/api/logout");
  },

  me: async (): Promise<UserInfo> => {
    const res = await api.get<UserInfo>("/api/me");
    return res.data;
  },
};

// CRUD 예시
export const TodoApi = {
  getList: async (): Promise<Todo[]> => {
    const res = await api.get("/api/todo");
    return res.data;
  },
  create: async (data: CreateTodo, csrfToken: string): Promise<Todo> => {
    const res = await api.post("/api/todo", data, {
      headers: { "X-CSRF-Token": csrfToken },
    });
    return res.data;
  },
  update: async (id: number, data: Partial<Todo>, csrfToken: string): Promise<Todo> => {
    const res = await api.put(`/api/todo${id}/`, data, {
      headers: { "X-CSRF-Token": csrfToken },
    });
    return res.data;
  },
  remove: async (id: number, csrfToken: string): Promise<void> => {
    await api.delete(`/api/todo${id}/`, {
      headers: { "X-CSRF-Token": csrfToken },
    });
  },
};

import axios, { AxiosHeaders, type InternalAxiosRequestConfig } from "axios";
import type { CsrfToken } from "../types/index";
import type { UserInfo, User } from "../types/auth";
import { type Todo, type CreateTodo } from "../types/todo";
import { getCsrfToken } from "./csrf";

export const api = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL,
    withCredentials: true,
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
  },

  logout: async (): Promise<void> => {
    await api.post("/api/logout");
  },

  me: async (): Promise<UserInfo> => {
    const res = await api.get<UserInfo>("/api/me");
    return res.data;
  },
};

export const TodoApi = {
  getList: async (): Promise<Todo[]> => {
    const res = await api.get("/api/todo/");
    return res.data;
  },
  create: async (data: CreateTodo, csrfToken: string): Promise<Todo> => {
    const res = await api.post("/api/todo/", data, {
      headers: { "X-CSRF-Token": csrfToken },
    });
    return res.data;
  },
  update: async (id: string, data: Partial<Todo>, csrfToken: string): Promise<Todo> => {
    const res = await api.put(`/api/todo/${id}`, data, {
      headers: { "X-CSRF-Token": csrfToken },
    });
    return res.data;
  },
  remove: async (id: string, csrfToken: string): Promise<void> => {
    await api.delete(`/api/todo/${id}`, {
      headers: { "X-CSRF-Token": csrfToken },
    });
  },
};

api.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const method = (config.method ?? "get").toLowerCase();

    if (["post", "put", "patch", "delete"].includes(method)) {
      const csrf = getCsrfToken();

      if (csrf) {
        if (!config.headers) {
          config.headers = new AxiosHeaders();
        }
        (config.headers as AxiosHeaders).set("X-CSRF-Token", csrf);
      }
    }

    return config;
  },
  (error) => Promise.reject(error)
);
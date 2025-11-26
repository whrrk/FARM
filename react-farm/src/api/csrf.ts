import { api } from "./api";

let csrfToken: string | null = null;

// 최초 1회 가져오는 함수 (async)
export async function loadCsrfToken() {
  const res = await api.get("/csrf-token");
  csrfToken = res.data.csrf_token;
}

// sync getter
export function getCsrfToken() {
  return csrfToken;
}
import { createContext, useContext, useEffect, useState } from "react";
import { api } from "../api/api";
import type { CsrfToken } from "../types/index";

interface CsrfContextValue {
  csrfToken: string | null;
  refreshCsrf: () => Promise<void>;
}

const CsrfContext = createContext<CsrfContextValue | null>(null);

export function CsrfProvider({ children }: { children: React.ReactNode }) {
  const [csrfToken, setCsrfToken] = useState<string | null>(null);

  const loadToken = async () => {
    const res = await api.get<CsrfToken>("/api/csrf-token");
    setCsrfToken(res.data.csrf_token);
  };

  useEffect(() => {
    loadToken().catch(console.error);
  }, []);

  return (
    <CsrfContext.Provider value={{ csrfToken, refreshCsrf: loadToken }}>
      {children}
    </CsrfContext.Provider>
  );
}

export function useCsrf() {
  const ctx = useContext(CsrfContext);
  if (!ctx) throw new Error("useCsrf must be used within CsrfProvider");
  return ctx;
}

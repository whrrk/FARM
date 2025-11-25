/// <reference types="vite/client" />

interface ImportMetaEnv {
    readonly VITE_API_BASE_URL: string;
    // 여기에 추가하면 됨
  }
  
  interface ImportMeta {
    readonly env: ImportMetaEnv;
  }
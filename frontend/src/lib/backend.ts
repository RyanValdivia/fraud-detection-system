import "server-only";

// Solo se usa dentro de route handlers (app/api/**). Nunca importar desde
// un client component: API_KEY no debe llegar al navegador.

const API_URL = process.env.API_URL ?? "http://localhost:8000";
const API_KEY = process.env.API_KEY ?? "";

export class BackendError extends Error {
  status: number;
  detail: string;

  constructor(status: number, detail: string) {
    super(detail);
    this.status = status;
    this.detail = detail;
  }
}

async function backendFetch(path: string, init: RequestInit = {}) {
  const res = await fetch(`${API_URL}${path}`, {
    ...init,
    headers: {
      "x-api-key": API_KEY,
      "Content-Type": "application/json",
      ...init.headers,
    },
    cache: "no-store",
  });

  if (!res.ok) {
    let detail = res.statusText;
    try {
      const body = await res.json();
      detail = body.detail ?? JSON.stringify(body);
    } catch {
      // respuesta sin body JSON, quedarse con statusText
    }
    throw new BackendError(res.status, detail);
  }

  return res.json();
}

export function predictTransaction(payload: Record<string, unknown>) {
  return backendFetch("/predict", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function getTransaction(id: string) {
  return backendFetch(`/transactions/${encodeURIComponent(id)}`);
}

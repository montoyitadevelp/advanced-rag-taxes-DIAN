import { API_URL } from "../constants/main";
import type { RequestOptions } from "./types/api";


function buildUrl(url: string, params?: Record<string, string | number>): string {
  if (!params) return `${API_URL}${url}`;
  const query = new URLSearchParams(params as any).toString();
  return `${API_URL}${url}?${query}`;
}

async function request<T = any>(url: string, options: RequestOptions = {}): Promise<T> {
  const fullUrl = buildUrl(url, options.params);

  const response = await fetch(fullUrl, {
    method: options.method || 'GET',
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    body: options.body ? JSON.stringify(options.body) : undefined,
  });

  const contentType = response.headers.get('content-type');
  const isJson = contentType?.includes('application/json');

  const data = isJson ? await response.json() : await response.text();

  if (!response.ok) {
    throw new Error(data?.detail || data?.error || 'API request failed');
  }

  return data;
}

export const api = {
  get: <T = any>(url: string, params?: Record<string, string | number>) =>
    request<T>(url, { method: 'GET', params }),

  post: <T = any>(url: string, body?: any) =>
    request<T>(url, { method: 'POST', body }),

  put: <T = any>(url: string, body?: any) =>
    request<T>(url, { method: 'PUT', body }),

  patch: <T = any>(url: string, body?: any) =>
    request<T>(url, { method: 'PATCH', body }),

  delete: <T = any>(url: string) =>
    request<T>(url, { method: 'DELETE' }),
};
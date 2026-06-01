const API_URL = import.meta.env.VITE_API_URL;

type RequestOptions = RequestInit & {
    auth?: boolean;
};

export async function apiFetch<T>(path: string, options: RequestOptions = {}): Promise<T> {
    const headers = new Headers(options.headers);
    headers.set('Content-Type', 'application/json');

    if (options.auth) {
        const token = localStorage.getItem('access_token');
        if (token) {
            headers.set('Authorization', `Bearer ${token}`);
        }
    }

    const response = await fetch(`${API_URL}${path}`, {
        ...options,
        headers
    });

    if (!response.ok) {
        const error = await response.json().catch(() => ({
            message: 'Error inesperado'
        }));
        throw error;
    }
    if (response.status === 204) {
        return undefined as T;
    }

    return response.json();
}

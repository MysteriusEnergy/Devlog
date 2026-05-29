import { apiFetch } from './client';
import type { LoginRequest, LoginResponse, RegisterRequest, RegisterResponse } from '$lib/types/auth';

export function login(data: LoginRequest) {
    return apiFetch<LoginResponse>('/auth/login/', {
        method: 'POST',
        body: JSON.stringify(data)
    });
}

export function register(data: RegisterRequest) {
    return apiFetch<RegisterResponse>('/auth/register/', {
        method: 'POST',
        body: JSON.stringify(data)
    });
}

export function logout(refreshToken: string) {
    return apiFetch<void>('/auth/logout/', {
        method: 'POST',
        body: JSON.stringify({
            refresh_token: refreshToken
        })
    });
}
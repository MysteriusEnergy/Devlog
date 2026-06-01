import { apiFetch } from './client';
import type {
	CreateWorkSessionRequest,
	UpdateWorkSessionRequest,
	WorkSession,
	WorkSessionsFilters,
	WorkSessionsResponse
} from '$lib/types/work-session';

export function getWorkSessions(filters: WorkSessionsFilters = {}) {
	const params = new URLSearchParams();

	for (const [key, value] of Object.entries(filters)) {
		if (value !== undefined && value !== '') {
			params.set(key, String(value));
		}
	}

	const query = params.toString();

	return apiFetch<WorkSessionsResponse>(`/work-sessions/${query ? `?${query}` : ''}`, {
		auth: true
	});
}

export function createWorkSession(data: CreateWorkSessionRequest) {
	return apiFetch<WorkSession>('/work-sessions/', {
		method: 'POST',
		auth: true,
		body: JSON.stringify(data)
	});
}

export function updateWorkSession(id: string, data: UpdateWorkSessionRequest) {
	return apiFetch<WorkSession>(`/work-sessions/${id}/`, {
		method: 'PATCH',
		auth: true,
		body: JSON.stringify(data)
	});
}

export function deleteWorkSession(id: string) {
	return apiFetch<void>(`/work-sessions/${id}/`, {
		method: 'DELETE',
		auth: true
	});
}
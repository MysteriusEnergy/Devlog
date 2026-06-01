import { apiFetch } from './client';
import type { CreateProjectRequest, Project, UpdateProjectRequest } from '$lib/types/project';

export function getProjects() {
	return apiFetch<Project[]>('/projects/', {
		auth: true
	});
}

export function createProject(data: CreateProjectRequest) {
	return apiFetch<Project>('/projects/', {
		method: 'POST',
		auth: true,
		body: JSON.stringify(data)
	});
}

export function updateProject(id: string, data: UpdateProjectRequest) {
	return apiFetch<Project>(`/projects/${id}/`, {
		method: 'PATCH',
		auth: true,
		body: JSON.stringify(data)
	});
}

export function deleteProject(id: string) {
	return apiFetch<void>(`/projects/${id}/`, {
		method: 'DELETE',
		auth: true
	});
}
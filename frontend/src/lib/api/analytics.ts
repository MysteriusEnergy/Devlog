import { apiFetch } from './client';
import type { AnalyticsSummary } from '$lib/types/analytics';

export function getAnalyticsSummary() {
	return apiFetch<AnalyticsSummary>('/analytics/summary/', {
		auth: true
	});
}

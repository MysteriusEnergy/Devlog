<script lang="ts">
	import { goto } from '$app/navigation';
	import { resolve } from '$app/paths';
	import { logout } from '$lib/api/auth';
	import { getAnalyticsSummary } from '$lib/api/analytics';
	import { auth } from '$lib/stores/auth.svelte';
	import type { AnalyticsSummary } from '$lib/types/analytics';
	import { onMount } from 'svelte';
	import { getProjects } from '$lib/api/projects';
	import type { Project } from '$lib/types/project';

	let summary = $state<AnalyticsSummary | null>(null);
	let error = $state('');
	let loading = $state(false);
	let loadingSummary = $state(true);
	let projects = $state<Project[]>([]);

	onMount(() => {
		void initializePage();
	});

	async function initializePage() {
		auth.load();

		if (!auth.isAuthenticated) {
			await goto(resolve('/login'));
			return;
		}

		await loadSummary();
	}

	async function loadSummary() {
		error = '';
		loadingSummary = true;

		try {
			const [summaryResponse, projectsResponse] = await Promise.all([
				getAnalyticsSummary(),
				getProjects()
			]);

			summary = summaryResponse;
			projects = projectsResponse;
		} catch {
			error = 'No se pudieron cargar las métricas';
		} finally {
			loadingSummary = false;
		}
	}

	function getProjectName(projectId: string) {
		const project = projects.find((item) => item.id === projectId);
		return project?.name ?? 'Proyecto desconocido';
	}

	function getProjectColor(projectId: string) {
		const project = projects.find((item) => item.id === projectId);
		return project?.color ?? '#2563eb';
	}

	function getProjectPercent(totalMinutes: number) {
		const maxMinutes = Math.max(
			...(summary?.project_breakdown.map((item) => item.total_minutes) ?? [1]),
			1
		);

		return `${Math.max(8, Math.round((totalMinutes / maxMinutes) * 100))}%`;
	}

	function formatHours(minutes: number) {
		return (minutes / 60).toFixed(2);
	}

	async function handleLogout() {
		loading = true;

		try {
			if (auth.refreshToken) {
				await logout(auth.refreshToken);
			}
		} finally {
			auth.clear();
			loading = false;
			await goto(resolve('/login'));
		}
	}
</script>

<svelte:head>
	<title>Dashboard | DevLog</title>
</svelte:head>

<main class="dashboard-page">
	<section class="dashboard-header">
		<div>
			<p class="eyebrow">Dashboard</p>
			<h1>Resumen de tu tiempo</h1>
			<p>Una vista rápida para saber qué has trabajado y dónde conviene seguir.</p>
		</div>

		<nav class="dashboard-actions" aria-label="Navegación principal">
			<a class="primary-action" href={resolve('/work-sessions')}>Registrar sesión</a>
			<a class="secondary-action" href={resolve('/projects')}>Proyectos</a>
		</nav>
	</section>

	{#if error}
		<p class="alert-message">{error}</p>
	{/if}

	{#if loadingSummary}
		<section class="soft-panel">
			<p class="muted">Cargando métricas...</p>
		</section>
	{:else if summary}
		<section class="metric-grid" aria-label="Resumen de métricas">
			<article class="metric-card">
				<span>Total trabajado</span>
				<strong>{summary.total_hours}</strong>
				<small>horas registradas</small>
			</article>

			<article class="metric-card">
				<span>Esta semana</span>
				<strong>{formatHours(summary.weekly_minutes)}</strong>
				<small>horas activas</small>
			</article>

			<article class="metric-card">
				<span>Total acumulado</span>
				<strong>{summary.total_minutes}</strong>
				<small>minutos</small>
			</article>
		</section>

		<section class="breakdown-panel">
			<div class="section-heading">
				<div>
					<h2>Horas por proyecto</h2>
					<p>Distribución del tiempo registrado hasta ahora.</p>
				</div>
			</div>

			{#if summary.project_breakdown.length === 0}
				<div class="empty-state">
					<strong>Todavía no tienes sesiones registradas.</strong>
					<p>Crea una sesión para empezar a ver el desglose por proyecto.</p>
					<a class="primary-action" href={resolve('/work-sessions')}>Registrar primera sesión</a>
				</div>
			{:else}
				<ul class="breakdown-list">
					{#each summary.project_breakdown as item (item.project_id)}
						<li style={`--project-color: ${getProjectColor(item.project_id)};`}>
							<div class="project-row">
								<div>
									<span class="project-dot"></span>
									<strong>{getProjectName(item.project_id)}</strong>
								</div>
								<span>{formatHours(item.total_minutes)} h</span>
							</div>

							<div class="project-bar" aria-hidden="true">
								<span style={`width: ${getProjectPercent(item.total_minutes)};`}></span>
							</div>
						</li>
					{/each}
				</ul>
			{/if}
		</section>
	{/if}

	<div class="footer-actions">
		<button type="button" class="logout-button" onclick={handleLogout} disabled={loading}>
			{loading ? 'Cerrando sesión...' : 'Cerrar sesión'}
		</button>
	</div>
</main>

<style>
	.dashboard-page {
		display: grid;
		gap: 1rem;
	}

	.dashboard-header {
		display: grid;
		grid-template-columns: 1fr auto;
		align-items: end;
		gap: 1.5rem;
		border-color: #dce3ef;
		background: linear-gradient(135deg, rgba(17, 24, 39, 0.98), rgba(37, 99, 235, 0.92)), #172033;
		color: white;
		padding: 1.25rem;
	}

	.dashboard-header h1,
	.dashboard-header p {
		margin: 0;
	}

	.dashboard-header h1 {
		margin-top: 0.45rem;
		font-size: 2.4rem;
		line-height: 1.05;
	}

	.dashboard-header p:last-child {
		max-width: 560px;
		margin-top: 0.85rem;
		color: rgba(255, 255, 255, 0.78);
	}

	.eyebrow {
		color: #99f6e4;
		font-size: 0.82rem;
		font-weight: 800;
		text-transform: uppercase;
	}

	.dashboard-actions,
	.footer-actions {
		display: flex;
		flex-wrap: wrap;
		gap: 0.65rem;
		margin: 0;
	}

	.primary-action,
	.secondary-action {
		display: inline-flex;
		align-items: center;
		justify-content: center;
		min-height: 42px;
		border-radius: 8px;
		font-weight: 800;
		padding: 0.68rem 0.9rem;
		text-decoration: none;
	}

	.primary-action {
		background: #ffffff;
		color: #172033;
	}

	.secondary-action {
		border: 1px solid rgba(255, 255, 255, 0.42);
		color: white;
	}

	.alert-message {
		border: 1px solid #fecaca;
		border-radius: 8px;
		background: #fef2f2;
		color: #991b1b;
		padding: 0.85rem 1rem;
	}

	.soft-panel,
	.breakdown-panel {
		border-color: #dce3ef;
	}

	.metric-grid {
		display: grid;
		grid-template-columns: repeat(3, minmax(0, 1fr));
		gap: 1rem;
		border: 0;
		background: transparent;
		padding: 0;
	}

	.metric-card {
		display: grid;
		gap: 0.25rem;
		border: 1px solid #dce3ef;
		border-radius: 8px;
		background: white;
		padding: 1rem;
	}

	.metric-card span,
	.metric-card small,
	.muted,
	.section-heading p,
	.empty-state p {
		color: #64748b;
	}

	.metric-card strong {
		color: #111827;
		font-size: 2rem;
		line-height: 1;
	}

	.section-heading {
		display: flex;
		align-items: flex-start;
		justify-content: space-between;
		gap: 1rem;
		margin-bottom: 1rem;
	}

	.section-heading h2,
	.section-heading p {
		margin: 0;
	}

	.section-heading p {
		margin-top: 0.3rem;
	}

	.empty-state {
		display: grid;
		justify-items: start;
		gap: 0.45rem;
		border: 1px dashed #cbd5e1;
		border-radius: 8px;
		background: #f8fafc;
		padding: 1rem;
	}

	.empty-state .primary-action {
		margin-top: 0.3rem;
		background: #2563eb;
		color: white;
	}

	.breakdown-list {
		display: grid;
		gap: 0.85rem;
		margin: 0;
	}

	.breakdown-list li {
		border: 0;
		background: transparent;
		padding: 0;
	}

	.breakdown-list li + li {
		margin-top: 0;
	}

	.project-row {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 1rem;
		margin-bottom: 0.45rem;
	}

	.project-row div {
		display: flex;
		align-items: center;
		gap: 0.55rem;
		min-width: 0;
	}

	.project-row span:last-child {
		color: #334155;
		font-weight: 800;
		white-space: nowrap;
	}

	.project-dot {
		width: 0.72rem;
		height: 0.72rem;
		border-radius: 999px;
		background: var(--project-color);
	}

	.project-bar {
		height: 0.55rem;
		border-radius: 999px;
		background: #e2e8f0;
		overflow: hidden;
	}

	.project-bar span {
		display: block;
		height: 100%;
		border-radius: inherit;
		background: var(--project-color);
	}

	.logout-button {
		background: #e2e8f0;
		color: #172033;
	}

	@media (max-width: 760px) {
		.dashboard-header,
		.metric-grid {
			grid-template-columns: 1fr;
		}

		.dashboard-header h1 {
			font-size: 2rem;
		}
	}
</style>

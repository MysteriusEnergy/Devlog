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

<main>
	<h1>Dashboard</h1>
	<p>Sesión iniciada correctamente.</p>

	<nav>
		<a href={resolve('/projects')}>Ver proyectos</a>
		<a href={resolve('/work-sessions')}>Ver sesiones</a>
	</nav>

	{#if error}
		<p style="color: red;">{error}</p>
	{/if}

	{#if loadingSummary}
		<p>Cargando métricas...</p>
	{:else if summary}
		<section>
			<h2>Resumen</h2>

			<ul>
				<li>Total trabajado: {summary.total_hours} horas</li>
				<li>Esta semana: {(summary.weekly_minutes / 60).toFixed(2)} horas</li>
				<li>Total en minutos: {summary.total_minutes}</li>
			</ul>
		</section>

		<section>
			<h2>Horas por proyecto</h2>

			{#if summary.project_breakdown.length === 0}
				<p>Todavía no tienes sesiones registradas.</p>
			{:else}
				<ul>
					{#each summary.project_breakdown as item (item.project_id)}
						<li>
							{getProjectName(item.project_id)}: {(item.total_minutes / 60).toFixed(2)} horas
						</li>
					{/each}
				</ul>
			{/if}
		</section>
	{/if}

	<button type="button" onclick={handleLogout} disabled={loading}>
		{loading ? 'Cerrando sesión...' : 'Cerrar sesión'}
	</button>
</main>

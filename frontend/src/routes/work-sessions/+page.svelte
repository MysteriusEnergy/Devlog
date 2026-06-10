<script lang="ts">
	import { goto } from '$app/navigation';
	import { resolve } from '$app/paths';
	import { getProjects } from '$lib/api/projects';
	import {
		createWorkSession,
		deleteWorkSession,
		getWorkSessions,
		updateWorkSession
	} from '$lib/api/work-sessions';
	import { auth } from '$lib/stores/auth.svelte';
	import type { Project } from '$lib/types/project';
	import type { WorkSession } from '$lib/types/work-session';
	import { onMount } from 'svelte';

	let projects = $state<Project[]>([]);
	let sessions = $state<WorkSession[]>([]);

	let projectId = $state('');
	let date = $state(new Date().toISOString().slice(0, 10));
	let startTime = $state('09:00');
	let endTime = $state('10:00');
	let notes = $state('');

	let error = $state('');
	let loading = $state(true);
	let saving = $state(false);

	let editingSessionId = $state<string | null>(null);

	let editStartTime = $state('');
	let editEndTime = $state('');
	let editNotes = $state('');
	let updating = $state(false);

	let deletingSessionId = $state<string | null>(null);

	let filterProjectId = $state('');
	let filterDate = $state('');
	let filterFrom = $state('');
	let filterTo = $state('');

	let page = $state(1);
	let totalPages = $state(1);
	let totalSessions = $state(0);
	let perPage = $state(20);

	onMount(async () => {
		auth.load();

		if (!auth.isAuthenticated) {
			await goto(resolve('/login'));
			return;
		}

		await loadPageData();
	});

	async function loadPageData() {
		error = '';
		loading = true;

		try {
			const [projectsResponse, sessionsResponse] = await Promise.all([
				getProjects(),
				getWorkSessions({
					project_id: filterProjectId,
					date: filterDate,
					from: filterFrom,
					to: filterTo,
					page,
					per_page: perPage
				})
			]);

			projects = projectsResponse;
			sessions = sessionsResponse.data;

			page = sessionsResponse.pagination.page;
			perPage = sessionsResponse.pagination.per_page;
			totalPages = sessionsResponse.pagination.total_pages;
			totalSessions = sessionsResponse.pagination.total;

			if (projects.length > 0 && !projectId) {
				projectId = projects[0].id;
			}
		} catch {
			error = 'No se pudieron cargar los datos';
		} finally {
			loading = false;
		}
	}

	async function handleApplyFilters(event: SubmitEvent) {
		event.preventDefault();

		page = 1;
		await loadPageData();
	}

	async function handleClearFilters() {
		filterProjectId = '';
		filterDate = '';
		filterFrom = '';
		filterTo = '';
		page = 1;

		await loadPageData();
	}

	async function goToPreviousPage() {
		if (page <= 1) {
			return;
		}

		page = page - 1;
		await loadPageData();
	}

	async function goToNextPage() {
		if (page >= totalPages) {
			return;
		}

		page = page + 1;
		await loadPageData();
	}

	async function handleCreate(event: SubmitEvent) {
		event.preventDefault();

		if (!projectId) {
			error = 'Selecciona un proyecto';
			return;
		}

		error = '';
		saving = true;

		try {
			await createWorkSession({
				project_id: projectId,
				date,
				start_time: startTime,
				end_time: endTime,
				notes
			});

			notes = '';
			page = 1;
			await loadPageData();
		} catch {
			error = 'No se pudo crear la sesión';
		} finally {
			saving = false;
		}
	}

	function startEdit(session: WorkSession) {
		editingSessionId = session.id;
		editStartTime = session.start_time;
		editEndTime = session.end_time;
		editNotes = session.notes;
	}

	function cancelEdit() {
		editingSessionId = null;
		editStartTime = '';
		editEndTime = '';
		editNotes = '';
	}

	async function handleUpdate(event: SubmitEvent, sessionId: string) {
		event.preventDefault();

		error = '';
		updating = true;

		try {
			const updatedSession = await updateWorkSession(sessionId, {
				start_time: editStartTime,
				end_time: editEndTime,
				notes: editNotes
			});

			sessions = sessions.map((session) => (session.id === sessionId ? updatedSession : session));

			cancelEdit();
		} catch {
			error = 'No se pudo actualizar la sesión';
		} finally {
			updating = false;
		}
	}

	async function handleDelete(sessionId: string) {
		const confirmed = confirm('¿Seguro que quieres eliminar esta sesión?');

		if (!confirmed) {
			return;
		}

		error = '';
		deletingSessionId = sessionId;

		try {
			await deleteWorkSession(sessionId);
			await loadPageData();
		} catch {
			error = 'No se pudo eliminar la sesión';
		} finally {
			deletingSessionId = null;
		}
	}

	function getProject(projectId: string) {
		return projects.find((item) => item.id === projectId);
	}

	function getProjectName(projectId: string) {
		return getProject(projectId)?.name ?? 'Proyecto desconocido';
	}

	function getProjectColor(projectId: string) {
		return getProject(projectId)?.color ?? '#2563eb';
	}

	function formatDuration(minutes: number) {
		const hours = Math.floor(minutes / 60);
		const rest = minutes % 60;

		if (hours === 0) {
			return `${rest}m`;
		}

		if (rest === 0) {
			return `${hours}h`;
		}

		return `${hours}h ${String(rest).padStart(2, '0')}m`;
	}
</script>

<svelte:head>
	<title>Sesiones | DevLog</title>
</svelte:head>

<main class="sessions-page">
	<section class="page-header">
		<a class="back-link" href={resolve('/dashboard')}>Volver al dashboard</a>

		<div class="title-row">
			<div>
				<h1>Sesiones de trabajo</h1>
				<p>Registra bloques, consulta el historial y ajusta tu tiempo sin perder contexto.</p>
			</div>

			<a class="secondary-action" href={resolve('/projects')}>Proyectos</a>
		</div>
	</section>

	{#if error}
		<p class="alert-message">{error}</p>
	{/if}

	{#if loading}
		<section class="soft-panel">
			<p class="muted">Cargando sesiones...</p>
		</section>
	{:else}
		<div class="tools-grid">
			<section class="session-panel">
				<div class="section-heading">
					<h2>Crear sesión</h2>
					<p>Registra el bloque actual o uno que acabas de cerrar.</p>
				</div>

				{#if projects.length === 0}
					<div class="empty-state">
						<strong>Primero necesitas un proyecto.</strong>
						<p>
							Las sesiones se guardan dentro de un proyecto para que las métricas tengan sentido.
						</p>
						<a class="primary-action" href={resolve('/projects')}>Crear proyecto</a>
					</div>
				{:else}
					<form class="session-form" onsubmit={handleCreate}>
						<div class="form-grid">
							<label class="wide-field">
								Proyecto
								<select bind:value={projectId} required>
									<option value="">Selecciona un proyecto</option>
									{#each projects as project (project.id)}
										<option value={project.id}>{project.name}</option>
									{/each}
								</select>
							</label>

							<label>
								Fecha
								<input bind:value={date} type="date" required />
							</label>

							<label>
								Inicio
								<input bind:value={startTime} type="time" required />
							</label>

							<label>
								Fin
								<input bind:value={endTime} type="time" required />
							</label>
						</div>

						<label>
							Notas
							<textarea bind:value={notes}></textarea>
						</label>

						<div class="form-actions">
							<button type="submit" disabled={saving}>
								{saving ? 'Guardando...' : 'Crear sesión'}
							</button>
						</div>
					</form>
				{/if}
			</section>

			<section class="filter-panel">
				<div class="section-heading">
					<h2>Filtros</h2>
					<p>Encuentra sesiones por proyecto o rango de fechas.</p>
				</div>

				<form class="filter-form" onsubmit={handleApplyFilters}>
					<div class="filters-grid">
						<label>
							Proyecto
							<select bind:value={filterProjectId}>
								<option value="">Todos los proyectos</option>
								{#each projects as project (project.id)}
									<option value={project.id}>{project.name}</option>
								{/each}
							</select>
						</label>

						<label>
							Fecha exacta
							<input bind:value={filterDate} type="date" />
						</label>

						<label>
							Desde
							<input bind:value={filterFrom} type="date" />
						</label>

						<label>
							Hasta
							<input bind:value={filterTo} type="date" />
						</label>
					</div>

					<div class="form-actions">
						<button type="submit">Aplicar filtros</button>
						<button type="button" class="secondary-button" onclick={handleClearFilters}>
							Limpiar filtros
						</button>
					</div>
				</form>
			</section>
		</div>

		<section class="sessions-section">
			<div class="sessions-heading">
				<div>
					<h2>Historial</h2>
					<p>Sesiones registradas según los filtros actuales.</p>
				</div>

				<span class="count-pill">{totalSessions} sesiones</span>
			</div>

			{#if sessions.length === 0}
				<div class="empty-state">
					<strong>Todavía no tienes sesiones.</strong>
					<p>Crea una sesión para empezar a construir tu historial de trabajo.</p>
				</div>
			{:else}
				<ul class="session-list">
					{#each sessions as session (session.id)}
						<li
							class="session-card"
							style={`--project-color: ${getProjectColor(session.project_id)};`}
						>
							{#if editingSessionId === session.id}
								<form class="edit-form" onsubmit={(event) => handleUpdate(event, session.id)}>
									<div class="session-card-top">
										<div class="session-title">
											<span class="session-color"></span>
											<div>
												<strong>{getProjectName(session.project_id)}</strong>
												<p class="session-meta">{session.date}</p>
											</div>
										</div>
									</div>

									<div class="compact-grid">
										<label>
											Inicio
											<input bind:value={editStartTime} type="time" required />
										</label>

										<label>
											Fin
											<input bind:value={editEndTime} type="time" required />
										</label>
									</div>

									<label>
										Notas
										<textarea bind:value={editNotes}></textarea>
									</label>

									<div class="actions">
										<button type="submit" disabled={updating}>
											{updating ? 'Guardando...' : 'Guardar'}
										</button>

										<button type="button" class="secondary-button" onclick={cancelEdit}>
											Cancelar
										</button>
									</div>
								</form>
							{:else}
								<div class="session-card-top">
									<div class="session-title">
										<span class="session-color"></span>
										<div>
											<strong>{getProjectName(session.project_id)}</strong>
											<p class="session-meta">
												{session.date} · {session.start_time} - {session.end_time}
											</p>
										</div>
									</div>

									<span class="session-duration">{formatDuration(session.duration_minutes)}</span>
								</div>

								{#if session.notes}
									<p class="session-notes">{session.notes}</p>
								{:else}
									<p class="muted">Sin notas.</p>
								{/if}

								<div class="actions">
									<button type="button" class="secondary-button" onclick={() => startEdit(session)}>
										Editar
									</button>

									<button
										type="button"
										class="danger-button"
										onclick={() => handleDelete(session.id)}
										disabled={deletingSessionId === session.id}
									>
										{deletingSessionId === session.id ? 'Eliminando...' : 'Eliminar'}
									</button>
								</div>
							{/if}
						</li>
					{/each}
				</ul>

				<div class="pagination">
					<button
						type="button"
						class="secondary-button"
						onclick={goToPreviousPage}
						disabled={page <= 1}
					>
						Anterior
					</button>

					<span class="pagination-status">Página {page} de {totalPages}</span>

					<button
						type="button"
						class="secondary-button"
						onclick={goToNextPage}
						disabled={page >= totalPages}
					>
						Siguiente
					</button>
				</div>
			{/if}
		</section>
	{/if}
</main>

<style>
	.sessions-page {
		display: grid;
		gap: 1rem;
	}

	.page-header,
	.session-panel,
	.filter-panel,
	.soft-panel {
		border-color: #dce3ef;
	}

	.page-header {
		display: grid;
		gap: 1rem;
	}

	.title-row,
	.sessions-heading,
	.session-card-top,
	.form-actions,
	.actions,
	.pagination {
		display: flex;
		align-items: flex-start;
		gap: 1rem;
	}

	.title-row,
	.sessions-heading,
	.session-card-top {
		justify-content: space-between;
	}

	.title-row h1,
	.title-row p,
	.section-heading h2,
	.section-heading p,
	.sessions-heading h2,
	.sessions-heading p,
	.session-meta,
	.session-notes,
	.muted {
		margin: 0;
	}

	.title-row h1 {
		color: #111827;
		font-size: 2.2rem;
		line-height: 1.1;
	}

	.title-row p,
	.section-heading p,
	.sessions-heading p,
	.muted,
	.session-meta,
	.empty-state p {
		color: #64748b;
	}

	.secondary-action,
	.primary-action {
		display: inline-flex;
		align-items: center;
		justify-content: center;
		min-height: 42px;
		border-radius: 8px;
		font-weight: 800;
		padding: 0.68rem 0.9rem;
		text-decoration: none;
		white-space: nowrap;
	}

	.secondary-action {
		border: 1px solid #cbd5e1;
		background: white;
		color: #172033;
	}

	.primary-action {
		background: #2563eb;
		color: white;
	}

	.alert-message {
		border: 1px solid #fecaca;
		border-radius: 8px;
		background: #fef2f2;
		color: #991b1b;
		padding: 0.85rem 1rem;
	}

	.tools-grid {
		display: grid;
		grid-template-columns: minmax(0, 1.1fr) minmax(320px, 0.9fr);
		align-items: start;
		gap: 1rem;
	}

	.section-heading {
		display: grid;
		gap: 0.3rem;
		margin-bottom: 1rem;
	}

	.session-form,
	.filter-form,
	.edit-form {
		border: 0;
		background: transparent;
		padding: 0;
	}

	.form-grid,
	.filters-grid,
	.compact-grid {
		display: grid;
		gap: 0.85rem;
	}

	.form-grid {
		grid-template-columns: repeat(3, minmax(0, 1fr));
	}

	.wide-field {
		grid-column: 1 / -1;
	}

	.filters-grid {
		grid-template-columns: repeat(2, minmax(0, 1fr));
	}

	.compact-grid {
		grid-template-columns: repeat(2, minmax(0, 1fr));
	}

	.form-actions,
	.actions,
	.pagination {
		flex-wrap: wrap;
		align-items: center;
	}

	.empty-state {
		display: grid;
		justify-items: start;
		gap: 0.4rem;
		border: 1px dashed #cbd5e1;
		border-radius: 8px;
		background: #f8fafc;
		padding: 1rem;
	}

	.empty-state strong {
		color: #111827;
	}

	.sessions-section {
		border: 0;
		background: transparent;
		padding: 0;
	}

	.sessions-heading {
		align-items: center;
		margin-bottom: 0.85rem;
	}

	.count-pill {
		border: 1px solid #cbd5e1;
		border-radius: 999px;
		background: #f8fafc;
		color: #334155;
		font-size: 0.88rem;
		font-weight: 800;
		padding: 0.4rem 0.7rem;
		white-space: nowrap;
	}

	.session-list {
		display: grid;
		gap: 0.85rem;
		margin: 0;
	}

	.session-list li + li {
		margin-top: 0;
	}

	.session-card {
		border-color: #dce3ef;
		box-shadow: 0 12px 30px rgba(15, 23, 42, 0.04);
	}

	.session-title {
		display: flex;
		gap: 0.75rem;
		min-width: 0;
	}

	.session-title strong {
		color: #111827;
	}

	.session-color {
		flex: 0 0 auto;
		width: 0.75rem;
		height: 2.4rem;
		border-radius: 999px;
		background: var(--project-color);
	}

	.session-duration {
		border-radius: 999px;
		background: #dbeafe;
		color: #1d4ed8;
		font-size: 0.88rem;
		font-weight: 800;
		padding: 0.35rem 0.65rem;
		white-space: nowrap;
	}

	.session-notes,
	.muted {
		margin-top: 0.75rem;
	}

	.session-notes {
		color: #334155;
		line-height: 1.55;
	}

	.session-card > .actions {
		margin-top: 0.85rem;
		border-top: 1px solid #e2e8f0;
		padding-top: 0.85rem;
	}

	.secondary-button {
		background: #e2e8f0;
		color: #172033;
	}

	.danger-button {
		background: #dc2626;
	}

	.pagination {
		justify-content: center;
		margin-top: 1rem;
	}

	.pagination-status {
		color: #64748b;
		font-weight: 700;
	}

	@media (max-width: 960px) {
		.tools-grid,
		.form-grid {
			grid-template-columns: 1fr;
		}

		.filters-grid {
			grid-template-columns: repeat(2, minmax(0, 1fr));
		}
	}

	@media (max-width: 620px) {
		.title-row,
		.sessions-heading,
		.session-card-top {
			display: grid;
			justify-content: stretch;
		}

		.filters-grid,
		.compact-grid {
			grid-template-columns: 1fr;
		}
	}
</style>

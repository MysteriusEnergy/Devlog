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

	function getProjectName(projectId: string) {
		const project = projects.find((item) => item.id === projectId);
		return project?.name ?? 'Proyecto desconocido';
	}
</script>

<main>
	<a href={resolve('/dashboard')}>Volver al dashboard</a>

	<h1>Work Sessions</h1>

	{#if error}
		<p style="color: red;">{error}</p>
	{/if}

	{#if loading}
		<p>Cargando...</p>
	{:else}
		<section>
			<h2>Crear sesión</h2>

			{#if projects.length === 0}
				<p>Primero necesitas crear un proyecto.</p>
				<a href={resolve('/projects')}>Crear proyecto</a>
			{:else}
				<form onsubmit={handleCreate}>
					<label>
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
						Hora inicio
						<input bind:value={startTime} type="time" required />
					</label>

					<label>
						Hora fin
						<input bind:value={endTime} type="time" required />
					</label>

					<label>
						Notas
						<textarea bind:value={notes}></textarea>
					</label>

					<button type="submit" disabled={saving}>
						{saving ? 'Guardando...' : 'Crear sesión'}
					</button>
				</form>
			{/if}
		</section>

		<section>
			<h2>Filtros</h2>

			<form onsubmit={handleApplyFilters}>
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

				<button type="submit">Aplicar filtros</button>

				<button type="button" onclick={handleClearFilters}> Limpiar filtros </button>
			</form>
		</section>

		<section>
			<h2>Sesiones</h2>
			<p>Total de sesiones: {totalSessions}</p>

			{#if sessions.length === 0}
				<p>Todavía no tienes sesiones.</p>
			{:else}
				<ul>
					{#each sessions as session (session.id)}
						<li>
							{#if editingSessionId === session.id}
								<form onsubmit={(event) => handleUpdate(event, session.id)}>
									<p>
										<strong>{getProjectName(session.project_id)}</strong>
									</p>

									<p>Fecha: {session.date}</p>

									<label>
										Hora inicio
										<input bind:value={editStartTime} type="time" required />
									</label>

									<label>
										Hora fin
										<input bind:value={editEndTime} type="time" required />
									</label>

									<label>
										Notas
										<textarea bind:value={editNotes}></textarea>
									</label>

									<button type="submit" disabled={updating}>
										{updating ? 'Guardando...' : 'Guardar'}
									</button>

									<button type="button" onclick={cancelEdit}> Cancelar </button>
								</form>
							{:else}
								<strong>{getProjectName(session.project_id)}</strong>

								<p>
									{session.date} · {session.start_time} - {session.end_time}
								</p>

								<p>
									Duración: {session.duration_minutes} minutos
								</p>

								{#if session.notes}
									<p>{session.notes}</p>
								{/if}

								<button type="button" onclick={() => startEdit(session)}> Editar </button>

								<button
									type="button"
									onclick={() => handleDelete(session.id)}
									disabled={deletingSessionId === session.id}
								>
									{deletingSessionId === session.id ? 'Eliminando...' : 'Eliminar'}
								</button>
							{/if}
						</li>
					{/each}
				</ul>

				<div>
					<button type="button" onclick={goToPreviousPage} disabled={page <= 1}> Anterior </button>

					<span>Página {page} de {totalPages}</span>

					<button type="button" onclick={goToNextPage} disabled={page >= totalPages}>
						Siguiente
					</button>
				</div>
			{/if}
		</section>
	{/if}
</main>

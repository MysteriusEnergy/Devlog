<script lang="ts">
	import { goto } from '$app/navigation';
	import { resolve } from '$app/paths';
	import { createProject, deleteProject, getProjects, updateProject } from '$lib/api/projects';
	import { auth } from '$lib/stores/auth.svelte';
	import type { Project } from '$lib/types/project';
	import { onMount } from 'svelte';

	let projects = $state<Project[]>([]);

	let name = $state('');
	let description = $state('');
	let color = $state('#2563eb');

	let error = $state('');
	let loading = $state(true);
	let saving = $state(false);

	let editingProjectId = $state<string | null>(null);
	let editName = $state('');
	let editDescription = $state('');
	let editColor = $state('#2563eb');
	let updating = $state(false);
	let deletingProjectId = $state<string | null>(null);

	onMount(async () => {
		auth.load();

		if (!auth.isAuthenticated) {
			await goto(resolve('/login'));
			return;
		}

		await loadProjects();
	});

	async function loadProjects() {
		error = '';
		loading = true;

		try {
			projects = await getProjects();
		} catch {
			error = 'No se pudieron cargar los proyectos';
		} finally {
			loading = false;
		}
	}

	async function handleCreate(event: SubmitEvent) {
		event.preventDefault();

		error = '';
		saving = true;

		try {
			const project = await createProject({
				name,
				description,
				color
			});

			projects = [project, ...projects];

			name = '';
			description = '';
			color = '#2563eb';
		} catch {
			error = 'No se pudo crear el proyecto';
		} finally {
			saving = false;
		}
	}

	function startEdit(project: Project) {
		editingProjectId = project.id;
		editName = project.name;
		editDescription = project.description;
		editColor = project.color;
	}

	function cancelEdit() {
		editingProjectId = null;
		editName = '';
		editDescription = '';
		editColor = '#2563eb';
	}

	async function handleUpdate(event: SubmitEvent, projectId: string) {
		event.preventDefault();

		error = '';
		updating = true;

		try {
			const updatedProject = await updateProject(projectId, {
				name: editName,
				description: editDescription,
				color: editColor
			});

			projects = projects.map((project) => (project.id === projectId ? updatedProject : project));

			cancelEdit();
		} catch {
			error = 'No se pudo actualizar el proyecto';
		} finally {
			updating = false;
		}
	}

	async function handleDelete(projectId: string) {
		const confirmed = confirm('¿Seguro que quieres eliminar este proyecto?');

		if (!confirmed) {
			return;
		}

		error = '';
		deletingProjectId = projectId;

		try {
			await deleteProject(projectId);
			projects = projects.filter((project) => project.id !== projectId);
		} catch {
			error = 'No se pudo eliminar el proyecto';
		} finally {
			deletingProjectId = null;
		}
	}
</script>

<svelte:head>
	<title>Proyectos | DevLog</title>
</svelte:head>

<main class="projects-page">
	<section class="page-header">
		<a class="back-link" href={resolve('/dashboard')}>Volver al dashboard</a>

		<div class="title-row">
			<div>
				<h1>Proyectos</h1>
				<p>Organiza tus iniciativas y usa colores para reconocerlas rápido.</p>
			</div>

			<span class="count-pill">{projects.length} proyectos</span>
		</div>
	</section>

	{#if error}
		<p class="alert-message">{error}</p>
	{/if}

	<div class="projects-layout">
		<section class="form-panel">
			<div class="section-heading">
				<h2>Crear proyecto</h2>
				<p>Solo necesitas un nombre; la descripción puede esperar.</p>
			</div>

			<form class="project-form" onsubmit={handleCreate}>
				<div class="name-color-grid">
					<label>
						Nombre
						<input bind:value={name} required />
					</label>

					<label class="color-field">
						Color
						<input bind:value={color} type="color" />
					</label>
				</div>

				<label>
					Descripción
					<textarea bind:value={description}></textarea>
				</label>

				<button type="submit" disabled={saving}>
					{saving ? 'Guardando...' : 'Crear proyecto'}
				</button>
			</form>
		</section>

		<section class="project-list-section">
			<div class="section-heading list-heading">
				<div>
					<h2>Tus proyectos</h2>
					<p>La lista que usarás para clasificar cada sesión.</p>
				</div>
			</div>

			{#if loading}
				<div class="soft-panel">
					<p class="muted">Cargando proyectos...</p>
				</div>
			{:else if projects.length === 0}
				<div class="empty-state">
					<strong>Todavía no tienes proyectos.</strong>
					<p>Crea el primero para poder registrar sesiones de trabajo.</p>
				</div>
			{:else}
				<ul class="project-list">
					{#each projects as project (project.id)}
						<li class="project-card" style={`--project-color: ${project.color};`}>
							{#if editingProjectId === project.id}
								<form class="edit-form" onsubmit={(event) => handleUpdate(event, project.id)}>
									<div class="name-color-grid">
										<label>
											Nombre
											<input bind:value={editName} required />
										</label>

										<label class="color-field">
											Color
											<input bind:value={editColor} type="color" />
										</label>
									</div>

									<label>
										Descripción
										<textarea bind:value={editDescription}></textarea>
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
								<div class="project-card-header">
									<div class="project-title">
										<span class="project-color"></span>
										<div>
											<strong>{project.name}</strong>
											{#if project.description}
												<p>{project.description}</p>
											{:else}
												<p class="muted">Sin descripción.</p>
											{/if}
										</div>
									</div>
								</div>

								<div class="actions project-actions">
									<button type="button" class="secondary-button" onclick={() => startEdit(project)}>
										Editar
									</button>

									<button
										type="button"
										class="danger-button"
										onclick={() => handleDelete(project.id)}
										disabled={deletingProjectId === project.id}
									>
										{deletingProjectId === project.id ? 'Eliminando...' : 'Eliminar'}
									</button>
								</div>
							{/if}
						</li>
					{/each}
				</ul>
			{/if}
		</section>
	</div>
</main>

<style>
	.projects-page {
		display: grid;
		gap: 1rem;
	}

	.page-header,
	.form-panel {
		border-color: #dce3ef;
	}

	.page-header {
		display: grid;
		gap: 1rem;
	}

	.title-row,
	.project-card-header,
	.actions {
		display: flex;
		align-items: flex-start;
		gap: 1rem;
	}

	.title-row {
		justify-content: space-between;
	}

	.title-row h1,
	.title-row p,
	.section-heading h2,
	.section-heading p,
	.project-title p {
		margin: 0;
	}

	.title-row h1 {
		color: #111827;
		font-size: 2.2rem;
		line-height: 1.1;
	}

	.title-row p,
	.section-heading p,
	.muted,
	.empty-state p {
		color: #64748b;
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

	.projects-layout {
		display: grid;
		grid-template-columns: minmax(300px, 0.8fr) minmax(0, 1.2fr);
		align-items: start;
		gap: 1rem;
	}

	.section-heading {
		display: grid;
		gap: 0.3rem;
		margin-bottom: 1rem;
	}

	.project-form,
	.edit-form {
		border: 0;
		background: transparent;
		padding: 0;
	}

	.name-color-grid {
		display: grid;
		grid-template-columns: minmax(0, 1fr) auto;
		gap: 0.85rem;
		align-items: end;
	}

	.color-field input {
		width: 4.25rem;
		height: 2.75rem;
		padding: 0.2rem;
	}

	.project-list-section {
		border: 0;
		background: transparent;
		padding: 0;
	}

	.list-heading {
		margin: 0 0 0.85rem;
	}

	.alert-message {
		border: 1px solid #fecaca;
		border-radius: 8px;
		background: #fef2f2;
		color: #991b1b;
		padding: 0.85rem 1rem;
	}

	.soft-panel,
	.empty-state {
		border: 1px solid #dce3ef;
		border-radius: 8px;
		background: white;
		padding: 1rem;
	}

	.empty-state {
		display: grid;
		gap: 0.35rem;
		border-style: dashed;
		background: #f8fafc;
	}

	.project-list {
		display: grid;
		gap: 0.85rem;
		margin: 0;
	}

	.project-list li + li {
		margin-top: 0;
	}

	.project-card {
		border-color: #dce3ef;
		box-shadow: 0 12px 30px rgba(15, 23, 42, 0.04);
	}

	.project-card-header {
		justify-content: space-between;
	}

	.project-title {
		display: flex;
		gap: 0.75rem;
		min-width: 0;
	}

	.project-title strong {
		color: #111827;
	}

	.project-color {
		flex: 0 0 auto;
		width: 0.8rem;
		height: 2.5rem;
		border-radius: 999px;
		background: var(--project-color);
	}

	.actions {
		flex-wrap: wrap;
		justify-content: flex-start;
	}

	.project-actions {
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

	@media (max-width: 860px) {
		.projects-layout,
		.title-row,
		.project-card-header {
			grid-template-columns: 1fr;
		}

		.projects-layout {
			display: grid;
		}

		.title-row,
		.project-card-header {
			display: grid;
		}

		.actions {
			justify-content: flex-start;
		}
	}

	@media (max-width: 560px) {
		.name-color-grid {
			grid-template-columns: 1fr;
		}

		.color-field input {
			width: 100%;
		}
	}
</style>

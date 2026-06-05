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

<main>
	<section class="page-header">
		<a href={resolve('/dashboard')}>Volver al dashboard</a>
		<h1>Proyectos</h1>
		<p>Organiza tus proyectos y usa colores para identificarlos rápidamente.</p>
	</section>

	<section>
		<h2>Crear proyecto</h2>

		<form onsubmit={handleCreate}>
			<label>
				Nombre
				<input bind:value={name} required />
			</label>

			<label>
				Descripción
				<textarea bind:value={description}></textarea>
			</label>

			<label>
				Color
				<input bind:value={color} type="color" />
			</label>

			<button type="submit" disabled={saving}>
				{saving ? 'Guardando...' : 'Crear proyecto'}
			</button>
		</form>
	</section>

	{#if error}
		<p style="color: red;">{error}</p>
	{/if}

	<section>
		<h2>Tus proyectos</h2>

		{#if loading}
			<p>Cargando proyectos...</p>
		{:else if projects.length === 0}
			<p>Todavía no tienes proyectos.</p>
		{:else}
			<ul class="project-list">
				{#each projects as project (project.id)}
					<li class="project-card">
						{#if editingProjectId === project.id}
							<form onsubmit={(event) => handleUpdate(event, project.id)}>
								<label>
									Nombre
									<input bind:value={editName} required />
								</label>

								<label>
									Descripción
									<textarea bind:value={editDescription}></textarea>
								</label>

								<label>
									Color
									<input bind:value={editColor} type="color" />
								</label>

								<div class="actions">
									<button type="submit" disabled={updating}>
										{updating ? 'Guardando...' : 'Guardar'}
									</button>

									<button type="button" class="secondary-button" onclick={cancelEdit}
										>Cancelar</button
									>
								</div>
							</form>
						{:else}
							<div class="project-title">
								<span class="project-color" style={`background: ${project.color};`}></span>
								<strong>{project.name}</strong>
							</div>

							{#if project.description}
								<p>{project.description}</p>
							{:else}
								<p class="muted">Sin descripción.</p>
							{/if}

							<div class="actions">
								<button type="button" onclick={() => startEdit(project)}>Editar</button>

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
</main>

<style>
	.page-header h1 {
		margin-bottom: 0.25rem;
	}

	.page-header p,
	.muted {
		color: #64748b;
	}

	.project-list {
		display: grid;
		gap: 1rem;
	}

	.project-card {
		display: grid;
		gap: 0.75rem;
	}

	.project-title {
		display: flex;
		align-items: center;
		gap: 0.5rem;
	}

	.project-color {
		display: inline-block;
		width: 0.8rem;
		height: 0.8rem;
		border-radius: 999px;
	}

	.actions {
		display: flex;
		flex-wrap: wrap;
		gap: 0.5rem;
	}

	.secondary-button {
		background: #e2e8f0;
		color: #172033;
	}

	.danger-button {
		background: #dc2626;
	}
</style>

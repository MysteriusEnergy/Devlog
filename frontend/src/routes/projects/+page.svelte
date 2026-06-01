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

			projects = projects.map((project) =>
				project.id === projectId ? updatedProject : project
			);

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
	<a href={resolve('/dashboard')}>Volver al dashboard</a>

	<h1>Projects</h1>

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

	{#if error}
		<p style="color: red;">{error}</p>
	{/if}

	{#if loading}
		<p>Cargando proyectos...</p>
	{:else if projects.length === 0}
		<p>Todavía no tienes proyectos.</p>
	{:else}
		<ul>
			{#each projects as project (project.id)}
				<li>
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

							<button type="submit" disabled={updating}>
								{updating ? 'Guardando...' : 'Guardar'}
							</button>

							<button type="button" onclick={cancelEdit}>
								Cancelar
							</button>
						</form>
					{:else}
						<span style={`color: ${project.color};`}>●</span>
						<strong>{project.name}</strong>

						{#if project.description}
							<p>{project.description}</p>
						{/if}

						<button type="button" onclick={() => startEdit(project)}>
							Editar
						</button>

						<button
							type="button"
							onclick={() => handleDelete(project.id)}
							disabled={deletingProjectId === project.id}
						>
							{deletingProjectId === project.id ? 'Eliminando...' : 'Eliminar'}
						</button>
					{/if}
				</li>
			{/each}
		</ul>
	{/if}
</main>
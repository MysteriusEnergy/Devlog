<script lang="ts">
	import { goto } from '$app/navigation';
	import { resolve } from '$app/paths';
	import { register } from '$lib/api/auth';

	let email = $state('');
	let password = $state('');
	let confirmPassword = $state('');
	let error = $state('');
	let loading = $state(false);

	async function handleSubmit(event: SubmitEvent) {
		event.preventDefault();

		error = '';

		if (password !== confirmPassword) {
			error = 'Las contraseñas no coinciden';
			return;
		}

		loading = true;

		try {
			await register({ email, password });
			await goto(resolve('/login'));
		} catch {
			error = 'No se pudo crear la cuenta';
		} finally {
			loading = false;
		}
	}
</script>

<svelte:head>
	<title>Crear cuenta | DevLog</title>
</svelte:head>

<main class="auth-page">
	<section class="auth-aside" aria-label="Resumen de DevLog">
		<p class="auth-kicker">DevLog</p>
		<h1>Empieza con un sistema simple para medir tu foco.</h1>
		<p>
			Crea tu espacio, separa proyectos por color y empieza a convertir sesiones en métricas claras.
		</p>

		<div class="auth-preview" aria-hidden="true">
			<div class="auth-preview-header">
				<span>Primera semana</span>
				<strong>12h 20m</strong>
			</div>

			<div class="auth-session-line">
				<span class="auth-dot teal"></span>
				<div>
					<strong>Proyectos listos</strong>
					<small>Organizados por color</small>
				</div>
			</div>

			<div class="auth-session-line">
				<span class="auth-dot blue"></span>
				<div>
					<strong>Sesiones registradas</strong>
					<small>Historial consultable</small>
				</div>
			</div>

			<div class="auth-progress">
				<span style="width: 52%;"></span>
			</div>
		</div>
	</section>

	<section class="auth-card">
		<a class="back-link" href={resolve('/')}>Volver al inicio</a>

		<div class="auth-header">
			<h1>Crear cuenta</h1>
			<p>Crea tu espacio para empezar a registrar proyectos y sesiones de trabajo.</p>
		</div>

		<form onsubmit={handleSubmit}>
			<label>
				Correo electrónico
				<input bind:value={email} type="email" autocomplete="email" required />
			</label>

			<label>
				Contraseña
				<input
					bind:value={password}
					type="password"
					autocomplete="new-password"
					required
					minlength="3"
				/>
			</label>

			<label>
				Confirmar contraseña
				<input
					bind:value={confirmPassword}
					type="password"
					autocomplete="new-password"
					required
					minlength="3"
				/>
			</label>

			{#if error}
				<p class="error-message">{error}</p>
			{/if}

			<button type="submit" disabled={loading}>
				{loading ? 'Creando cuenta...' : 'Crear cuenta'}
			</button>
		</form>

		<p class="auth-switch">
			¿Ya tienes cuenta?
			<a href={resolve('/login')}>Inicia sesión</a>
		</p>
	</section>
</main>

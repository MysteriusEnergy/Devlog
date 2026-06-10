<script lang="ts">
	import { goto } from '$app/navigation';
	import { resolve } from '$app/paths';
	import { login } from '$lib/api/auth';
	import { auth } from '$lib/stores/auth.svelte';

	let email = $state('');
	let password = $state('');
	let error = $state('');
	let loading = $state(false);

	async function handleSubmit(event: SubmitEvent) {
		event.preventDefault();

		error = '';
		loading = true;

		try {
			const response = await login({ email, password });

			auth.setTokens(response.access_token, response.refresh_token);

			await goto(resolve('/dashboard'));
		} catch {
			error = 'Credenciales inválidas o error de conexión';
		} finally {
			loading = false;
		}
	}
</script>

<svelte:head>
	<title>Iniciar sesión | DevLog</title>
</svelte:head>

<main class="auth-page">
	<section class="auth-aside" aria-label="Resumen de DevLog">
		<p class="auth-kicker">DevLog</p>
		<h1>Vuelve directo a tu ritmo de trabajo.</h1>
		<p>
			Revisa proyectos, sesiones y métricas sin reconstruir tu día desde notas sueltas o memoria.
		</p>

		<div class="auth-preview" aria-hidden="true">
			<div class="auth-preview-header">
				<span>Hoy</span>
				<strong>4h 45m</strong>
			</div>

			<div class="auth-session-line">
				<span class="auth-dot blue"></span>
				<div>
					<strong>Producto MVP</strong>
					<small>09:00 - 11:10</small>
				</div>
			</div>

			<div class="auth-session-line">
				<span class="auth-dot amber"></span>
				<div>
					<strong>Diseño UI</strong>
					<small>11:30 - 13:00</small>
				</div>
			</div>

			<div class="auth-progress">
				<span style="width: 68%;"></span>
			</div>
		</div>
	</section>

	<section class="auth-card">
		<a class="back-link" href={resolve('/')}>Volver al inicio</a>

		<div class="auth-header">
			<h1>Iniciar sesión</h1>
			<p>Entra a tu dashboard para revisar proyectos, sesiones y métricas.</p>
		</div>

		<form onsubmit={handleSubmit}>
			<label>
				Correo electrónico
				<input bind:value={email} type="email" autocomplete="email" required />
			</label>

			<label>
				Contraseña
				<input bind:value={password} type="password" autocomplete="current-password" required />
			</label>

			{#if error}
				<p class="error-message">{error}</p>
			{/if}

			<button type="submit" disabled={loading}>
				{loading ? 'Ingresando...' : 'Ingresar'}
			</button>
		</form>

		<p class="auth-switch">
			¿No tienes cuenta?
			<a href={resolve('/register')}>Crear cuenta</a>
		</p>
	</section>
</main>

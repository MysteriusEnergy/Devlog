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

<main class="auth-page">
	<section class="auth-card">
		<a class="back-link" href={resolve('/')}>Volver al inicio</a>

		<div class="auth-header">
			<h1>Iniciar sesión</h1>
			<p>Entra a tu dashboard para revisar proyectos, sesiones y métricas.</p>
		</div>

		<form onsubmit={handleSubmit}>
			<label>
				Email
				<input bind:value={email} type="email" autocomplete="email" required />
			</label>

			<label>
				Password
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

<script lang="ts">
	import { goto } from '$app/navigation';
    import { resolve } from '$app/paths';
	import { login } from '$lib/api/auth';
	import { auth } from '$lib/stores/auth.svelte';

	let email = $state('');
	let password = $state('');
	let error = $state('');
	let loading = $state(false);

	// Agregamos el event: Event para controlar el submit
	async function handleSubmit(event: Event) {
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

<main>
	<h1>Iniciar sesión</h1>

	<form onsubmit={handleSubmit}>
		<label>
			Email
			<input bind:value={email} type="email" required />
		</label>
		<label>
			Password
			<input bind:value={password} type="password" required />
		</label>

		{#if error}
			<p style="color: red;">{error}</p>
		{/if}

		<button type="submit" disabled={loading}>
			{loading ? 'Ingresando...' : 'Ingresar'}
		</button>
	</form>

	<p>
		¿No tienes cuenta?
		<a href={resolve('/register')}>Crear cuenta</a>
	</p>
</main>
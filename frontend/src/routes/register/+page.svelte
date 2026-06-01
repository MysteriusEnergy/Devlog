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

<main>
	<h1>Crear cuenta</h1>

	<form onsubmit={handleSubmit}>
		<label>
			Email
			<input bind:value={email} type="email" required />
		</label>

		<label>
			Password
			<input bind:value={password} type="password" required minlength="3" />
		</label>

		<label>
			Confirmar password
			<input bind:value={confirmPassword} type="password" required minlength="3" />
		</label>

		{#if error}
			<p style="color: red;">{error}</p>
		{/if}

		<button type="submit" disabled={loading}>
			{loading ? 'Creando cuenta...' : 'Crear cuenta'}
		</button>
	</form>

	<p>
		¿Ya tienes cuenta?
		<a href={resolve('/login')}>Inicia sesión</a>
	</p>
</main>

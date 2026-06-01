<script lang="ts">
	import { goto } from '$app/navigation';
	import { resolve } from '$app/paths';
	import { logout } from '$lib/api/auth';
	import { auth } from '$lib/stores/auth.svelte';
	import { onMount } from 'svelte';

	let loading = $state(false);

	onMount(() => {
		auth.load();

		if (!auth.isAuthenticated) {
			void goto(resolve('/login'));
		}
	});

	async function handleLogout() {
		loading = true;

		try {
			if (auth.refreshToken) {
				await logout(auth.refreshToken);
			}
		} finally {
			auth.clear();
			loading = false;
			await goto(resolve('/login'));
		}
	}
</script>

<main>
	<h1>Dashboard</h1>
	<p>Sesión iniciada correctamente.</p>

	<button type="button" onclick={handleLogout} disabled={loading}>
		{loading ? 'Cerrando sesión...' : 'Cerrar sesión'}
	</button>
</main>
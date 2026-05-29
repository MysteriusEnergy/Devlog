<script lang="ts">
	import { goto } from '$app/navigation';
	import { resolve } from '$app/paths';
	import { onMount } from 'svelte';

	onMount(() => {
		const token = localStorage.getItem('access_token');

		if (!token) {
			void goto(resolve('/login'));
		}
	});
</script>

<main>
	<h1>Dashboard</h1>
	<p>Sesion iniciada correctamente.</p>
</main>

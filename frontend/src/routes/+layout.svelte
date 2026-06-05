<script lang="ts">
	import favicon from '$lib/assets/favicon.svg';
	import { onMount } from 'svelte';
	import { auth } from '$lib/stores/auth.svelte';
	import '../app.css';

	// Esto es propio de Svelte 5 para renderizar las páginas
	let { children } = $props();

	// Tu lógica para revivir la sesión al cargar la app
	onMount(() => {
		auth.load();
	});
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
</svelte:head>

{@render children()}

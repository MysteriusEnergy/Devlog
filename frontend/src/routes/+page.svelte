-- Active: 1779736373265@@127.0.0.1@5432@devlog_db
<script lang="ts">
	import { resolve } from '$app/paths';
</script>

<main>
	<h1>DevLog</h1>
	<p>Registra proyectos, sesiones de trabajo y métricas de productividad.</p>

	<nav>
		<a href={resolve('/login')}>Iniciar sesión</a>
		<a href={resolve('/register')}>Crear cuenta</a>
	</nav>
</main>
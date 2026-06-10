<script lang="ts">
	import { resolve } from '$app/paths';
</script>

<main>
	<section class="landing-hero">
		<p class="eyebrow">DevLog</p>
		<h1>Controla tu tiempo de trabajo sin perder foco.</h1>
		<p>
			Registra proyectos, sesiones de trabajo y métricas para entender dónde inviertes tu tiempo.
		</p>

		<nav class="hero-actions">
			<a class="primary-link" href={resolve('/login')}>Iniciar sesión</a>
			<a class="secondary-link" href={resolve('/register')}>Crear cuenta</a>
		</nav>
	</section>

	<section class="feature-grid" aria-label="Funciones principales">
		<article>
			<strong>Proyectos</strong>
			<p>Organiza cada iniciativa con nombre, descripción y color.</p>
		</article>

		<article>
			<strong>Sesiones</strong>
			<p>Registra bloques de trabajo con fechas, horas y notas.</p>
		</article>

		<article>
			<strong>Métricas</strong>
			<p>Consulta horas totales, semana actual y desglose por proyecto.</p>
		</article>
	</section>
</main>

<style>
	.landing-hero {
		background: linear-gradient(135deg, #172033, #2563eb);
		color: white;
		padding: 3rem 1.5rem;
	}

	.landing-hero h1 {
		max-width: 720px;
		font-size: clamp(2.2rem, 8vw, 4.5rem);
		line-height: 1;
		margin: 0;
	}

	.landing-hero p {
		max-width: 640px;
		font-size: 1.1rem;
	}

	.eyebrow {
		font-weight: 700;
		letter-spacing: 0.12em;
		text-transform: uppercase;
	}

	.hero-actions {
		margin-top: 1.5rem;
	}

	.primary-link,
	.secondary-link {
		border-radius: 999px;
		font-weight: 700;
		padding: 0.75rem 1rem;
		text-decoration: none;
	}

	.primary-link {
		background: white;
		color: #172033;
	}

	.secondary-link {
		border: 1px solid rgba(255, 255, 255, 0.6);
		color: white;
	}

	.feature-grid {
		display: grid;
		gap: 1rem;
		grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
	}

	.feature-grid article {
		border: 1px solid #e1e6f0;
		border-radius: 16px;
		background: white;
		padding: 1rem;
	}

	.feature-grid p {
		color: #64748b;
	}
</style>

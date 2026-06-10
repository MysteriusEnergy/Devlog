<script lang="ts">
	import { resolve } from '$app/paths';
</script>

<svelte:head>
	<title>DevLog | Control de tiempo</title>
</svelte:head>

<main class="landing-page">
	<section class="product-intro" aria-labelledby="landing-title">
		<div class="intro-copy">
			<p class="eyebrow">DevLog</p>
			<h1 id="landing-title">Tu registro diario de trabajo, sin perder el hilo.</h1>
			<p class="intro-text">
				Registra sesiones, organiza proyectos y revisa dónde se va tu tiempo con una vista pensada
				para volver rápido al trabajo.
			</p>

			<nav class="hero-actions" aria-label="Acciones principales">
				<a class="primary-link" href={resolve('/login')}>Iniciar sesión</a>
				<a class="secondary-link" href={resolve('/register')}>Crear cuenta</a>
			</nav>
		</div>

		<div class="dashboard-preview" aria-label="Vista previa de DevLog">
			<div class="preview-toolbar">
				<div>
					<span class="preview-label">Semana actual</span>
					<strong>18h 45m</strong>
				</div>

				<span class="status-pill">En foco</span>
			</div>

			<div class="preview-metrics">
				<div>
					<span>Total</span>
					<strong>126h</strong>
				</div>

				<div>
					<span>Proyectos</span>
					<strong>8</strong>
				</div>

				<div>
					<span>Promedio</span>
					<strong>3h 40m</strong>
				</div>
			</div>

			<div class="preview-content">
				<div class="session-stack">
					<div class="session-row">
						<span class="project-dot product"></span>
						<div>
							<strong>Producto MVP</strong>
							<span>09:00 - 11:10</span>
						</div>
						<small>2h 10m</small>
					</div>

					<div class="session-row">
						<span class="project-dot design"></span>
						<div>
							<strong>Diseño UI</strong>
							<span>11:30 - 13:00</span>
						</div>
						<small>1h 30m</small>
					</div>

					<div class="session-row">
						<span class="project-dot api"></span>
						<div>
							<strong>API Analytics</strong>
							<span>15:00 - 16:05</span>
						</div>
						<small>1h 05m</small>
					</div>
				</div>

				<div class="weekly-panel">
					<div class="weekly-header">
						<span>Ritmo semanal</span>
						<strong>74%</strong>
					</div>

					<div class="bar-chart" aria-hidden="true">
						<span style="height: 42%;"></span>
						<span style="height: 65%;"></span>
						<span style="height: 54%;"></span>
						<span style="height: 82%;"></span>
						<span style="height: 70%;"></span>
					</div>
				</div>
			</div>
		</div>
	</section>

	<section class="workflow-strip" aria-label="Funciones principales">
		<article>
			<span class="feature-mark projects"></span>
			<strong>Proyectos claros</strong>
			<p>Clasifica cada iniciativa por nombre, color y descripción.</p>
		</article>

		<article>
			<span class="feature-mark sessions"></span>
			<strong>Sesiones rápidas</strong>
			<p>Guarda bloques de trabajo con fecha, horas y notas útiles.</p>
		</article>

		<article>
			<span class="feature-mark metrics"></span>
			<strong>Métricas accionables</strong>
			<p>Revisa totales, semana actual y desglose por proyecto.</p>
		</article>
	</section>
</main>

<style>
	.landing-page {
		display: grid;
		gap: 1.25rem;
		padding: 2rem 0 3rem;
	}

	.landing-page section {
		border: 0;
		border-radius: 0;
		background: transparent;
		padding: 0;
	}

	.product-intro {
		display: grid;
		grid-template-columns: minmax(0, 0.9fr) minmax(420px, 1.1fr);
		align-items: center;
		gap: 2rem;
		min-height: 560px;
	}

	.intro-copy {
		display: grid;
		gap: 1rem;
		align-content: center;
	}

	.eyebrow {
		margin: 0;
		color: #0f766e;
		font-size: 0.95rem;
		font-weight: 800;
		letter-spacing: 0;
		text-transform: uppercase;
	}

	.product-intro h1 {
		max-width: 640px;
		margin: 0;
		color: #111827;
		font-size: 4rem;
		line-height: 1;
	}

	.intro-text {
		max-width: 560px;
		margin: 0;
		color: #526071;
		font-size: 1.08rem;
		line-height: 1.65;
	}

	.hero-actions {
		margin: 0.5rem 0 0;
	}

	.primary-link,
	.secondary-link {
		display: inline-flex;
		align-items: center;
		justify-content: center;
		min-height: 44px;
		border-radius: 8px;
		font-weight: 800;
		padding: 0.72rem 1rem;
		text-decoration: none;
	}

	.primary-link {
		background: #111827;
		color: white;
		box-shadow: 0 14px 28px rgba(17, 24, 39, 0.16);
	}

	.secondary-link {
		border: 1px solid #cbd5e1;
		color: #172033;
		background: white;
	}

	.dashboard-preview {
		position: relative;
		display: grid;
		gap: 1rem;
		border: 1px solid #dce3ef;
		border-radius: 8px;
		background:
			linear-gradient(180deg, rgba(255, 255, 255, 0.95), rgba(255, 255, 255, 0.88)), #f8fafc;
		box-shadow: 0 28px 70px rgba(15, 23, 42, 0.12);
		padding: 1.15rem;
		overflow: hidden;
	}

	.dashboard-preview::before {
		content: '';
		position: absolute;
		inset: 0;
		background:
			linear-gradient(90deg, rgba(15, 118, 110, 0.08) 1px, transparent 1px),
			linear-gradient(180deg, rgba(37, 99, 235, 0.06) 1px, transparent 1px);
		background-size: 44px 44px;
		pointer-events: none;
	}

	.dashboard-preview > * {
		position: relative;
	}

	.preview-toolbar,
	.preview-metrics,
	.preview-content,
	.workflow-strip {
		display: grid;
		gap: 1rem;
	}

	.preview-toolbar {
		grid-template-columns: 1fr auto;
		align-items: center;
		border-bottom: 1px solid #e2e8f0;
		padding-bottom: 1rem;
	}

	.preview-toolbar strong {
		display: block;
		margin-top: 0.15rem;
		color: #111827;
		font-size: 2rem;
	}

	.preview-label,
	.preview-metrics span,
	.session-row span,
	.weekly-header span {
		color: #64748b;
		font-size: 0.88rem;
	}

	.status-pill {
		border: 1px solid rgba(15, 118, 110, 0.24);
		border-radius: 999px;
		background: #ccfbf1;
		color: #0f766e;
		font-size: 0.85rem;
		font-weight: 800;
		padding: 0.4rem 0.7rem;
	}

	.preview-metrics {
		grid-template-columns: repeat(3, 1fr);
	}

	.preview-metrics div,
	.weekly-panel {
		border: 1px solid #e2e8f0;
		border-radius: 8px;
		background: rgba(255, 255, 255, 0.86);
		padding: 0.9rem;
	}

	.preview-metrics strong {
		display: block;
		margin-top: 0.25rem;
		color: #111827;
		font-size: 1.35rem;
	}

	.preview-content {
		grid-template-columns: minmax(0, 1.25fr) minmax(180px, 0.75fr);
		align-items: stretch;
	}

	.session-stack {
		display: grid;
		gap: 0.75rem;
	}

	.session-row {
		display: grid;
		grid-template-columns: auto 1fr auto;
		align-items: center;
		gap: 0.75rem;
		border: 1px solid #e2e8f0;
		border-radius: 8px;
		background: white;
		padding: 0.85rem;
	}

	.session-row strong {
		display: block;
		color: #172033;
	}

	.session-row small {
		color: #334155;
		font-weight: 800;
		white-space: nowrap;
	}

	.project-dot,
	.feature-mark {
		display: inline-block;
		border-radius: 999px;
	}

	.project-dot {
		width: 0.75rem;
		height: 0.75rem;
	}

	.product {
		background: #2563eb;
	}

	.design {
		background: #f59e0b;
	}

	.api {
		background: #0f766e;
	}

	.weekly-panel {
		display: grid;
		align-content: space-between;
		min-height: 210px;
	}

	.weekly-header {
		display: flex;
		justify-content: space-between;
		gap: 1rem;
	}

	.weekly-header strong {
		color: #0f766e;
	}

	.bar-chart {
		display: grid;
		grid-template-columns: repeat(5, 1fr);
		align-items: end;
		gap: 0.45rem;
		height: 140px;
	}

	.bar-chart span {
		border-radius: 999px 999px 4px 4px;
		background: linear-gradient(180deg, #14b8a6, #2563eb);
		min-height: 28px;
	}

	.workflow-strip {
		grid-template-columns: repeat(3, 1fr);
		border: 1px solid #e1e6f0;
		border-radius: 8px;
		background: white;
		padding: 1rem;
	}

	.workflow-strip article {
		display: grid;
		gap: 0.55rem;
		border: 1px solid #e2e8f0;
		border-radius: 8px;
		background: #ffffff;
		padding: 1rem;
	}

	.workflow-strip strong {
		color: #111827;
	}

	.workflow-strip p {
		margin: 0;
		color: #64748b;
		line-height: 1.5;
	}

	.feature-mark {
		width: 2rem;
		height: 0.45rem;
		border-radius: 999px;
	}

	.feature-mark.projects {
		background: #2563eb;
	}

	.feature-mark.sessions {
		background: #f59e0b;
	}

	.feature-mark.metrics {
		background: #0f766e;
	}

	@media (max-width: 900px) {
		.product-intro {
			grid-template-columns: 1fr;
			min-height: auto;
		}

		.product-intro h1 {
			font-size: 3rem;
		}

		.dashboard-preview {
			order: -1;
		}
	}

	@media (max-width: 680px) {
		.landing-page {
			padding-top: 1rem;
		}

		.product-intro h1 {
			font-size: 2.35rem;
		}

		.preview-metrics,
		.preview-content,
		.workflow-strip {
			grid-template-columns: 1fr;
		}

		.preview-toolbar {
			grid-template-columns: 1fr;
		}

		.session-row {
			grid-template-columns: auto 1fr;
		}

		.session-row small {
			grid-column: 2;
		}
	}
</style>

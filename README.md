# AI-Agents-Lab
Laboratorio de investigación y experimentación para probar y evaluar agentes de IA, centrado en la comprensión del contexto, el seguimiento de instrucciones y la precisión de sus respuestas.

## Herramientas de evaluación

Para medir la calidad de los LLMs usamos tres herramientas, cada una con su suite en el repo:

| Herramienta | Suite | Qué aporta | Valoración |
|---|---|---|---|
| [Langfuse](https://langfuse.com/) | [`langfuse/`](langfuse/) | Datasets y experimentos en la nube: histórico de runs comparables, trazas completas de cada llamada (prompt, tokens, coste) y el razonamiento del juez en cada score. | ⭐⭐⭐⭐⭐ |
| [promptfoo](https://www.promptfoo.dev/) | [`promptfoo/`](promptfoo/) | Evals declarativos en YAML contra un LLM real, con asserts por caso y modelo juez; UI local de resultados (`npx promptfoo view`). | ⭐⭐⭐⭐ |
| [DeepEval](https://deepeval.com/) | [`deepeval/`](deepeval/) | Suites tipo pytest por agente; mide la calidad de respuesta y detecta datos inventados (alucinaciones) con la métrica **Faithfulness**. | ⭐⭐⭐ |

Valoración subjetiva (1–5 ⭐) según la experiencia de uso en este repo, ordenada de mayor a menor: **Langfuse** es el más completo — histórico comparable, trazas con coste y razonamiento del juez — a cambio de depender de un servicio externo; **promptfoo** es el más rápido de montar y su UI local es muy cómoda, aunque exige Node ≥ 22; a **DeepEval** le penalizan las fricciones de ejecución (hay que correrlo desde su carpeta por el shadowing del paquete y su resumen propio cuenta los canarios como fallos).

El README de cada suite explica cómo lanzarla y qué resultado esperar.

## Alcance y licencia

Este es un **proyecto experimental de testing, análisis y estudio** — no es software de producción. Los agentes, plantillas, datos y escenarios del repositorio son ficticios y existen solo con fines de investigación y aprendizaje.

El código se publica bajo licencia [MIT](LICENSE), sin garantía de ningún tipo.

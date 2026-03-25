# Idea Capture Repo

This repository is a personal idea capture and planning tool. When the user describes an idea, help them capture it quickly and cleanly.

## Repo Structure

- `ideas/` — Raw idea captures. One markdown file per idea.
- `plans/` — Structured plans expanded from ideas.
- `templates/` — Templates for ideas and plans.

## Conventions

- **Idea files**: `ideas/YYYY-MM-DD-slug.md` (e.g., `ideas/2026-03-25-rain-powered-garden-sensor.md`)
- **Plan files**: `plans/YYYY-MM-DD-slug.md` (same slug as the idea it expands)
- **Slugs**: lowercase, hyphen-separated, short but descriptive

## Slash Commands

- `/idea` — Capture a new idea from a conversational description
- `/plan` — Expand an existing idea into a structured plan
- `/status` — Dashboard summary of ideas and plans: counts, freshness, staleness
- `/review` — Revisit old ideas, surface unplanned ones, flag stale ones
- `/refine` — Tighten up an existing idea or plan with more detail or sharper thinking
- `/brainstorm` — Riff on a topic and generate multiple idea files at once
- `/pitch` — Turn a plan into a shareable elevator pitch
- `/link` — Connect related ideas and plans together

## Behavior Guidelines

- When capturing ideas, use today's date and generate a concise slug from the idea
- Keep the tone casual and authentic — preserve the user's voice and excitement
- Don't over-formalize raw ideas; save structure for plans
- When creating a plan, always link back to the original idea file
- When refining, preserve the original structure and the user's voice
- When linking, use relative markdown paths and avoid duplicate links
- Commit and push after creating/updating files

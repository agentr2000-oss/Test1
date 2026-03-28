# Idea Capture Repo

This repository is a personal idea capture and planning tool. When the user describes an idea, help them capture it quickly and cleanly.

## Repo Structure

- `ideas/` — Raw idea captures. One markdown file per idea.
- `plans/` — Structured plans expanded from ideas.
- `legal-analyses/` — Structured legal analyses and document reviews.
- `templates/` — Templates for ideas and plans.

## Conventions

- **Idea files**: `ideas/YYYY-MM-DD-slug.md` (e.g., `ideas/2026-03-25-rain-powered-garden-sensor.md`)
- **Plan files**: `plans/YYYY-MM-DD-slug.md` (same slug as the idea it expands)
- **Legal analysis files**: `legal-analyses/YYYY-MM-DD-slug.md`
- **Slugs**: lowercase, hyphen-separated, short but descriptive

## Slash Commands

- `/idea` — Capture a new idea from a conversational description
- `/plan` — Expand an existing idea into a structured plan
- `/legal-analysis` — Analyze a legal topic or review a legal document

## Behavior Guidelines

- When capturing ideas, use today's date and generate a concise slug from the idea
- Keep the tone casual and authentic — preserve the user's voice and excitement
- Don't over-formalize raw ideas; save structure for plans
- When creating a plan, always link back to the original idea file
- Legal analyses must always include the disclaimer. Flag uncertain citations with [NEEDS VERIFICATION]. Warn before committing sensitive legal documents.
- Commit and push after creating/updating files

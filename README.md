# Idea Capture

A personal repo for capturing ideas on the go and spinning them into actionable plans.

## How it works

1. **Capture** — When an idea hits, run `/idea` in Claude Code and describe it. A formatted idea file gets created, committed, and pushed.
2. **Plan** — When you're ready to think deeper, run `/plan` to expand any idea into a structured plan with approach, components, open questions, and next steps.
3. **Grow** — Use `/review`, `/refine`, `/brainstorm`, `/link`, `/status`, and `/pitch` to revisit, connect, and sharpen your ideas over time.

## Structure

```
ideas/          Raw idea captures (one file per idea)
plans/          Structured plans expanded from ideas
templates/      Templates for ideas and plans
.claude/commands/   Slash commands for Claude Code
```

## Slash Commands

| Command | What it does |
|---------|-------------|
| `/idea` | Capture a new idea from a quick description |
| `/plan` | Expand an existing idea into a structured plan |
| `/status` | Dashboard summary: counts, freshness, staleness |
| `/review` | Revisit old ideas, surface unplanned ones, flag stale ones |
| `/refine` | Tighten up an existing idea or plan |
| `/brainstorm` | Riff on a topic and generate multiple ideas at once |
| `/pitch` | Turn a plan into a shareable elevator pitch |
| `/link` | Connect related ideas and plans together |

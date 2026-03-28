# Idea Capture

A personal repo for capturing ideas on the go and spinning them into actionable plans.

## How it works

1. **Capture** — When an idea hits, run `/idea` in Claude Code and describe it. A formatted idea file gets created, committed, and pushed.
2. **Plan** — When you're ready to think deeper, run `/plan` to expand any idea into a structured plan with approach, components, open questions, and next steps.
3. **Review** — Run `/review_plan` to gut-check a plan for completeness and actionability before executing.

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
| `/review_plan` | Review a plan for quality, completeness, and actionability |

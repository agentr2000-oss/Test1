# Idea Capture

A personal repo for capturing ideas on the go and spinning them into actionable plans.

## How it works

1. **Capture** — When an idea hits, run `/idea` in Claude Code and describe it. A formatted idea file gets created, committed, and pushed.
2. **Plan** — When you're ready to think deeper, run `/plan` to expand any idea into a structured plan with approach, components, open questions, and next steps.
3. **Analyze** — For legal questions or documents, run `/legal-analysis` to get a structured analysis covering issues, applicable law, risks, gaps, and recommended actions.

## Structure

```
ideas/          Raw idea captures (one file per idea)
plans/          Structured plans expanded from ideas
legal-analyses/ Structured legal analyses and document reviews
templates/      Templates for ideas and plans
.claude/commands/   Slash commands for Claude Code
```

## Slash Commands

| Command | What it does |
|---------|-------------|
| `/idea` | Capture a new idea from a quick description |
| `/plan` | Expand an existing idea into a structured plan |
| `/legal-analysis` | Analyze a legal topic or review a legal document |

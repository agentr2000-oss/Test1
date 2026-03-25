Show a dashboard summary of the ideas and plans in this repo.

## Instructions

1. Scan the `ideas/` directory and count all idea files (exclude .gitkeep)
2. Scan the `plans/` directory and count all plan files (exclude .gitkeep)
3. For each idea, check whether a matching plan exists (same slug)
4. Categorize ideas as:
   - **Planned** — has a corresponding plan file
   - **Unplanned** — no plan yet
   - **Stale** — older than 30 days with no plan
5. Display a summary like:
   - Total ideas: X
   - Total plans: X
   - Unplanned ideas: X
   - Stale ideas (30+ days, no plan): X
6. List the 5 most recent ideas with their status
7. If there are stale or unplanned ideas, suggest running `/review` or `/plan`

This is read-only — don't create, modify, or commit any files.

$ARGUMENTS

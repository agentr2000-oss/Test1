Revisit old ideas and surface ones that need attention.

## Instructions

1. List all idea files in the `ideas/` directory
2. For each idea, determine:
   - Whether it has a corresponding plan in `plans/` (matched by slug)
   - How old it is (from the date in the filename)
3. If the user provided a specific topic or filter in their arguments, narrow the list accordingly
4. Present ideas grouped by status:
   - **Unplanned** — ideas with no plan yet (suggest running `/plan` on promising ones)
   - **Stale** — ideas older than 30 days with no plan (ask if they should be archived or expanded)
   - **Planned** — ideas that already have plans (briefly note these for completeness)
5. For each unplanned or stale idea, read the file and give a one-sentence reminder of what it's about
6. Ask the user what they'd like to do: plan one, refine one, archive one, or just move on

This is read-only — don't create, modify, or commit any files unless the user asks to take action.

$ARGUMENTS

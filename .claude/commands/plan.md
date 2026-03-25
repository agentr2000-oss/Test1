Expand an existing idea into a structured plan.

## Instructions

1. If the user specifies an idea, find it in the `ideas/` directory. If not, list recent ideas and ask which one to expand.
2. Read the idea file to understand the full context.
3. Create a plan file: `plans/YYYY-MM-DD-slug.md` (use the same slug as the idea)
4. Fill in the plan template from `templates/plan.md`:
   - Write a clear problem statement grounded in the idea's notes
   - Propose a concrete approach — be specific but not over-engineered
   - Break it into 3-5 key components or phases
   - List resources realistically
   - Surface the most important open questions as checkboxes
   - Suggest 2-3 actionable next steps the user could start today
5. Commit with message: "plan: {short description}"
6. Push to the current branch

Be thoughtful but practical. The plan should make the idea feel achievable, not intimidating.

$ARGUMENTS

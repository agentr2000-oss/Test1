Review an existing plan for quality, completeness, and actionability.

## Instructions

1. If the user specifies a plan, find it in the `plans/` directory. If not, list existing plans and ask which one to review.
2. Read the plan file thoroughly.
3. Follow the idea link in the plan header and read the original idea file — make sure the plan actually addresses what the idea was about.
4. Evaluate the plan and share your review:
   - **Alignment** — Does the plan stay true to the original idea's intent?
   - **Completeness** — Are all sections filled in meaningfully? Flag any that feel thin or templated.
   - **Specificity** — Is the approach concrete enough to act on, or is it vague?
   - **Scope** — Is this achievable, or has it ballooned into something unrealistic?
   - **Next Steps** — Could someone start on step 1 today?
   - **Open Questions** — Are the right questions being asked? Any obvious ones missing?
5. For each dimension, note whether the plan is **over-specced** (too detailed/rigid for this stage) or **under-specced** (too vague to act on). A good plan hits the sweet spot.
6. Summarize with a verdict: **Ready to go**, **Needs work**, or **Major rethink**.
7. Ask the user if they'd like you to apply the suggested improvements to the plan.
8. If yes, update the plan file with the improvements — keep the same structure, just make it stronger.
9. If the plan was updated, commit with message: "review: tighten up {slug}" and push to the current branch.

Be honest but encouraging. The goal is to make the plan stronger, not to tear it apart.

$ARGUMENTS

Riff on a topic and generate multiple idea files at once.

## Instructions

1. Take the user's topic or prompt from their arguments. If no arguments, ask what they want to brainstorm about.
2. Generate 3-5 distinct idea angles on the topic. For each angle, come up with a different take — vary the approach, audience, scale, or domain.
3. Present the ideas as a numbered list with a title and one-liner for each. Ask the user which ones to keep (or say "all").
4. For each idea the user wants to keep, create an idea file following the standard process:
   - Generate a slug for each idea
   - Use today's date: `ideas/YYYY-MM-DD-slug.md`
   - Fill in the template from `templates/idea.md`
   - Keep notes authentic and exploratory — brainstorm energy, not polished prose
5. Commit all new idea files together with message: "brainstorm: {topic} ({N} ideas)"
6. Push to the current branch

Go wide, not deep. The point is divergent thinking — capture the sparks and refine later.

$ARGUMENTS

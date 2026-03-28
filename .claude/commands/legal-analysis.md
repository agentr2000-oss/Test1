Perform a legal analysis on a topic or document.

## Instructions

1. Determine the input:
   - If the user provides a **file path**, read the file in full. Treat as a **Document Review**.
   - If the user provides a **description or pasted text** about a legal topic, treat as a **Topic Analysis**.
   - If unclear, ask the user to clarify.

2. **Confidentiality check:** If the input appears to contain sensitive legal content (client names, case numbers, privileged information), warn the user that committing it to git will create a permanent record. Ask if they want to proceed or redact first.

3. Identify the jurisdiction. Use what the user stated, infer from the document if obvious, or ask.

4. Perform a structured multi-pass analysis:

   **Pass 1 — Issue Spotting:** Identify every discrete legal issue. Number them. Cast a wide net — better to flag a minor issue than miss one.

   **Pass 2 — Legal Framework:** For each issue, identify applicable law (statutes, regulations, case law). Note jurisdiction and cross-jurisdictional conflicts. Track key precedents and their current status (affirmed, overruled, distinguished). Flag any citation you are not certain about with **[NEEDS VERIFICATION]**.

   **Pass 3 — Strengths, Weaknesses, and Counterarguments:** For each issue, assess the position honestly. Steel-man the opposing side.

   **Pass 4 — Gaps, Ambiguities, Risk, and Deadlines:** Identify what is **missing** (topics not addressed, provisions absent) and what is **uncertain** (vague language, unsettled law, multiple interpretations). Rank each by priority (High/Medium/Low). Assess risk likelihood and severity. Note any statutory deadlines, filing windows, or limitation periods. If regulatory compliance is involved, build a compliance checklist.

   **For Document Review specifically:** Do both:
   - **Clause-by-clause breakdown:** Walk through the document sequentially, quoting key language from each section and flagging issues inline. Fill the "Document Review — Clause-by-Clause Breakdown" template section.
   - **Issue-based analysis:** Also organize findings by legal issue in the standard sections above (Applicable Law, Analysis of Positions, etc.) so the analysis is navigable both ways.

5. Generate a concise slug. Use today's date: `legal-analyses/YYYY-MM-DD-slug.md`

6. Fill the template from `templates/legal-analysis.md`:
   - Write a plain-language executive summary a non-lawyer can understand
   - Complete every applicable section
   - Remove optional sections if they don't apply: Document Review Clause-by-Clause (topic analysis only), Precedent Tracker, Timeline & Deadlines, Compliance Checklist
   - Use **[NEEDS VERIFICATION]** liberally on citations
   - The Disclaimer section is mandatory — never remove or weaken it

7. Commit with message: "legal-analysis: {short description}"
8. Push to the current branch

## Guidance

- Be thorough. Legal analysis rewards completeness over brevity.
- Be honest about uncertainty. If the law is unsettled, say so.
- Do not invent case citations. Flag anything uncertain with **[NEEDS VERIFICATION]**.
- Expand beyond the user's framing — part of the value is spotting issues they didn't think of.
- The disclaimer must always be included.

$ARGUMENTS

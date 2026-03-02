The student is asking for help with their current task.

## Setup

Read `lab/.progress.json` to determine:
- `current_module`: which module they're on
- `current_challenge`: which challenge they're working on (e.g., "0.2")

If `current_challenge` is empty or not set:
- "You don't have an active challenge. Run `/lab:module N` to start or resume a module."

Read `.claude/commands/lab/flows/module-{current_module}.md` and find the Hints section
for the current challenge.

## Hint Progression

Track hint level **per challenge** in conversation memory. Reset when the student moves to a new challenge.

**First `/lab:hint`** — Concept Hint
- Explain the underlying principle without giving the answer
- Use **Hint 1 (Concept)** from the flow file
- "Think about how [concept] works in this context..."

**Second `/lab:hint`** — Approach Hint
- Suggest the general methodology or starting point
- Use **Hint 2 (Approach)** from the flow file
- "Try looking at [specific area]. What command would help?"

**Third `/lab:hint`** — Specific Hint
- Give specific steps, but let the student execute
- Use **Hint 3 (Specific)** from the flow file
- "Run `[command]` and look for [specific thing]"

**Fourth+ `/lab:hint`** — Walkthrough Offer
- "You've used all three hints for this challenge. Would you like me to walk you through it step by step?"
- Note: A full walkthrough won't award points for self-completion.

## Rules

- NEVER jump straight to the specific hint. Always start with concept.
- After providing a hint, always end with a question that nudges the student toward the answer.
- If the student is stuck on **infrastructure** (not concepts), you can be more direct with technical help. Infra problems are not learning objectives.
- Note: Using hints may reduce quiz scoring during verification (informational, not punitive).

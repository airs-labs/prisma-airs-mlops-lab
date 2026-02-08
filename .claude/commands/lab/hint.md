The student is asking for help with their current task.

Read lab/.progress.json to determine:
- current_module: which module they're on
- current_challenge: which challenge they're working on (e.g. "0.2")
- modules.{current_module}.hint_count: how many hints they've used

Read .claude/commands/lab/flows/module-{current_module}.md and find the Hints section
for the current challenge.

Provide a PROGRESSIVE hint based on how many times they've asked for help on this topic:

**First hint request**: High-level conceptual direction
- Use **Hint 1 (Concept)** from the flow file
- Point them to relevant documentation or code files

**Second hint request**: More specific approach guidance
- Use **Hint 2 (Approach)** from the flow file
- Give them a concrete starting direction

**Third hint request**: Near-complete guidance
- Use **Hint 3 (Specific)** from the flow file
- Show them the pattern but let them apply it

**Fourth+ hint request**: Provide the answer
- Show the complete solution
- But ALWAYS explain WHY, not just WHAT

Increment hint_count in lab/.progress.json for the current module.
Note: Using hints reduces quiz scores (hint -> 1 point max per question instead of 3).

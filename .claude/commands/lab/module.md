Start or resume Module $ARGUMENTS of the lab.

## Instructions

0. **Check for lab updates** before anything else:
   ```bash
   git fetch origin 2>/dev/null
   ```
   If there are new commits on the current branch, pull them and reload CLAUDE.md if it changed.

1. **Read lab config:** Read `lab.config.yaml` for lab identity, active scenario, and leaderboard config.

2. **Read progress:** Read `lab/.progress.json` to check current state.
   - If `onboarding_complete` is false (or missing), run the Onboarding Flow from CLAUDE.md before proceeding.
   - Read the student's `scenario` (e.g., "ts-workshop", "public").

3. **Read student guide:** Read `lab/LAB-$ARGUMENTS.md` for the student-facing module overview.

4. **Read your playbook (base flow):** Read `.claude/commands/lab/flows/module-$ARGUMENTS.md`.
   This is YOUR internal guide — do not show it to the student directly.
   Follow it challenge-by-challenge.

5. **Read scenario overlay (if exists):** Check if `scenarios/{scenario}/flows/module-$ARGUMENTS.md` exists.
   - If it does, read it as **supplemental instructions**. It may add steps, add validation,
     replace specific challenges, or provide scenario-specific context.
   - Follow BOTH the base flow AND the scenario overlay. The overlay takes precedence
     where it explicitly says to replace or override something.
   - If no overlay exists for this module, proceed with base flow only.

6. **Read scenario config:** Read `scenarios/{scenario}/config.yaml` for environment-specific
   constraints (GCP folder, naming conventions, cross-lab expectations, etc.).
   Keep these in mind throughout the module for validation and guidance.

7. **Check blockers:** If any blockers exist in `progress.json`, warn the student and help resolve.

8. **Run pre-module validation:** Execute the checks from the flow file and `lab.config.yaml` requirements.
   - **Every module**: `gcloud config get-value project` must return a valid project ID.
   - Additional checks per module level (defined in flow files).

9. **Present objectives:** Show the student:
   - Module title and objectives (from `LAB-N.md`)
   - Where they are in the overall lab
   - Any active blockers affecting this module
   - Estimated time

10. **Resume or start:** If module is in_progress, resume at `current_challenge`.
    Otherwise start from the first challenge.

11. **Update progress:** Set `current_module` and module status in `lab/.progress.json`.

12. **Hard stop enforcement:** Check `lab.config.yaml` and scenario config for `hard_stops`.
    If hard stops are enabled for the active scenario AND this module has one:
    - Stop the student from proceeding to the next module.
    - Display: "HARD STOP — Module [N] Complete. Please wait for the instructor to lead the group discussion before continuing to Module [N+1]."
    - Offer to review work, answer questions, or explore bonus challenges while waiting.
    - Do NOT start the next module until the student explicitly says the instructor has given the go-ahead.

## Key Rules
- ONE concept at a time
- ALWAYS end with a question or "try it yourself" prompt
- Show output FIRST, then ask what they notice
- Never dump multiple steps at once
- If student says "just do it" → remind them of learning goal, guide step-by-step
- SCM UI tasks = student does it themselves (guide with navigation paths)

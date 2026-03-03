# Module 5 Flow: Integrate AIRS into Pipeline

> INTERNAL PLAYBOOK — never shown to students.
> Engagement points tracked during module. All other scoring happens during /lab:verify-5.

## Points Available

| Source | Points | When |
|--------|--------|------|
| Engage: Bypass mechanisms — skip_scan vs --warn-only (5.1) | 1 | During flow |
| Engage: Three scans redundant or complementary? (5.3) | 1 | During flow |
| Engage: SDK gap — customer framing (5.5) | 1 | During flow |
| Technical: Gate 1 scanning enabled, policy fixed | 2 | During verify |
| Technical: Gate 2 scan added + manifest recording | 2 | During verify |
| Technical: Gate 3 scan added + manifest verification | 2 | During verify |
| Technical: Labels on scans in SCM | 2 | During verify |
| Technical: Evaluation summary in GH Actions | 2 | During verify |
| Quiz Q1: Source types and security groups | 3 | During verify |
| Quiz Q2: Scan failure flow | 3 | During verify |
| **Total** | **19** | |

---

## Preflight

Before starting, verify the student's environment:
1. AIRS SDK installed and credentials working (Module 4 prerequisite)
2. Security group UUIDs known (Default LOCAL, Default GCS, Default HuggingFace — from Module 4.2)
3. `MODEL_SECURITY_CLIENT_ID`, `MODEL_SECURITY_CLIENT_SECRET`, `TSG_ID` set as GitHub secrets

If any are missing, resolve before proceeding — these are hard blockers for pipeline scanning.

---

## Challenge 5.1: Gate 1 — Supply Chain Scan (HuggingFace Source)

### Learning Objectives

The student should be able to:
- Enable Gate 1 scanning by removing the `skip_scan` bypass used in earlier modules
- Investigate a governance BLOCK, distinguish it from a threat detection BLOCK, and fix the policy in SCM
- Explain HuggingFace source type scanning: 11 rules (7 threat detection + 4 governance), server-side scanning, metadata-dependent rules

### Key Concepts

Teach these BEFORE modifying the workflow. One at a time, wait for response.

1. **Gate 1's Scan Step Exists — You've Been Skipping It**
   - Core idea: Back in Module 2, the student triggered Gate 1 with `skip_scan=true` — scanning was deliberately bypassed because AIRS wasn't configured yet. Now it is. The scan step is already coded in `gate-1-train.yaml`: it calls `airs/scan_model.py` on the base model from HuggingFace. But there are TWO bypass mechanisms in the current code: the `skip_scan` input (skips the entire scan job) and a `--warn-only` flag (runs the scan but ignores BLOCKED verdicts). Both need to be addressed.
   - Show: Read `.github/workflows/gate-1-train.yaml` and display the scan job (starting at the `gate1-scan-base-model` job definition). Point out:
     - The `skip_scan` input and the `if: ${{ inputs.skip_scan != true }}` condition on the job
     - The `--warn-only` flag on the `scan_model.py` call (and the comment: "policy rules shouldn't block training")
     - The credentials from secrets: `MODEL_SECURITY_CLIENT_ID`, `MODEL_SECURITY_CLIENT_SECRET`, `TSG_ID`
     - The `--output-json` flag saving results for downstream processing
   - Check: Can the student explain what `skip_scan` does vs what `--warn-only` does? They're two different bypass mechanisms. Why were they there originally?

2. **Remove --warn-only, Enable Strict Scanning**
   - Core idea: `--warn-only` silently swallows BLOCKED verdicts — the scan runs, detects issues, but exits 0 anyway. This hides problems instead of surfacing them. The right approach: run strict, and when something blocks, investigate WHY and fix the ROOT CAUSE (the policy in SCM), not bypass the enforcement in the pipeline. Remove `--warn-only` from the Gate 1 scan step.
   - Note: also check if `--warn-only` appears elsewhere in the workflow (e.g., in the manifest recording step after training). Remove it there too.
   - After removing: if the student triggers Gate 1 now (without `skip_scan`), the scan will run strict. The base model is Qwen from HuggingFace. In Module 4, the student discovered Qwen is BLOCKED by governance rules. The same will happen here — the pipeline will fail.
   - Check: Can the student explain the difference between fixing the POLICY (in SCM — change which rules block vs alert) and bypassing the ENFORCEMENT (in the pipeline — --warn-only)? Which approach gives you visibility AND control?

3. **Fix the Qwen Policy — Trust the Org**
   - Core idea: Trigger Gate 1 without `skip_scan`, without `--warn-only`. Expected: scan runs, Qwen is BLOCKED. The student investigates — this is the same governance block from Module 4: license type `"other"` not in the approved list, and the Qwen organization not verified by HuggingFace. These are governance rules, not threat detection. All threat detection rules PASSED — the model is technically safe.
   - The student makes a policy decision. Two options:
     - **Option A (recommended):** Set both failing governance rules to non-blocking (alert mode). Detections still logged, still visible in SCM, but don't stop the pipeline. Bias: trust the org.
     - **Option B:** Add `other` to approved licenses and add Qwen to approved orgs. More permissive — explicitly whitelists.
   - Show: Navigate to SCM → Default HuggingFace security group. Find the two failing rules: "License Is Valid For Use" and "Organization Verified By HuggingFace." Show the enforcement mode toggle (blocking vs non-blocking).
   - After fix: re-trigger Gate 1 (or run a manual scan of Qwen). Expected: `eval_outcome: ALLOWED`, but `rules_failed: 2` — same detection, different enforcement. This is the key value prop from Module 4: **same detection, configurable enforcement.**
   - Check: After the fix, the scan still DETECTS the governance issues but doesn't BLOCK. Can the student explain this to a customer? When would you keep these rules in blocking mode?

> **ENGAGE**: "In Module 2, you used `skip_scan=true` to bypass scanning. The workflow also had `--warn-only` to silently swallow BLOCKED verdicts. These are two different bypass mechanisms. When would each be appropriate in a real enterprise pipeline?"
> Award 1 pt for meaningful engagement. No wrong answers — teach if needed.
> (Answer: `skip_scan` is for pre-approved models or when AIRS isn't configured yet — explicit, visible opt-out. `--warn-only` is more dangerous — scanning runs but problems are hidden. In production: neither should be the default. Use security group enforcement modes instead — alert in dev, block in prod.)

### Action

1. Read and modify `.github/workflows/gate-1-train.yaml`:
   - Remove `--warn-only` from the scan step (line ~159)
   - Check for and remove any other `--warn-only` flags in the workflow (e.g., manifest recording after training, line ~398)
2. Commit and push the workflow change
3. Trigger Gate 1 without `skip_scan` — observe the BLOCKED result
4. Fix the Qwen governance policy in SCM (set failing rules to non-blocking)
5. Re-trigger Gate 1 or re-scan Qwen manually — verify ALLOWED

### Debrief

- Gate 1 scans the **supply chain** — the base model coming from an external source. HuggingFace is special: models have metadata (license, org verification) that governance rules can validate. This is why HF security groups have 11 rules while LOCAL groups have only 7.
- The `--warn-only` lesson: don't hide problems in the pipeline. If a policy blocks something it shouldn't, fix the policy in SCM. If a model has a real threat, the block is doing its job.
- HuggingFace scanning is server-side — the SDK sends the request to the AIRS-HuggingFace partnership infrastructure. No local download, no disk space needed. The scan result comes back with `scan_origin: "HUGGING_FACE"`.
- Foreshadow Gate 2: "The base model is now trusted. But what about the model you BUILT from it? After merging adapter + base, is the artifact safe?"

### Deep Dive

For `/lab:explore`: `lab/topics/module-5/00-pipeline-scanning.md`

---

## Challenge 5.2: Gate 2 — Artifact Scan (Local Source)

### Learning Objectives

The student should be able to:
- Add an AIRS scan step to Gate 2 between the merge and publish steps
- Explain how the SDK detects source type from the model path and why LOCAL uses different rules than HuggingFace
- Record scan provenance in the manifest for downstream verification

### Key Concepts

Teach these BEFORE modifying the workflow. One at a time, wait for response.

1. **Where Scanning Fits in Gate 2**
   - Core idea: Gate 2 has two phases: merge (LoRA adapter + base model → merged safetensors, CPU-only) and publish (copy merged model to the approved GCS registry). The scan goes BETWEEN them — scan the artifact BEFORE it reaches the production registry. If the scan blocks, publish never runs. The compromised model never enters a location where Gate 3 could deploy it.
   - Show: Read `.github/workflows/gate-2-publish.yaml` and display:
     - The "Merge LoRA Adapter with Base Model" step (line ~203) — produces `./merged-model`, sets `MODEL_PATH=./merged-model` as env var
     - The "Publish to GCS" step (line ~216) — copies from `$MODEL_PATH` to `$GCS_BLESSED_BUCKET`
     - The scan step goes between these two. Use Gate 1's scan step as a reference pattern for credentials, output handling, and verdict parsing.
   - Check: Can the student identify the insertion point and explain why the scan MUST be before publish? What happens if a blocked model gets published?

2. **Source Type Detection: LOCAL vs HuggingFace**
   - Core idea: The merged model lives at `./merged-model` — a local directory on the GitHub Actions runner. The SDK detects this as `LOCAL` source type and auto-selects the Default LOCAL security group. LOCAL groups have 7 threat detection rules — no governance rules (no license/org checks). Why? Because a locally-built model has no supply chain metadata to validate. Gate 1 already checked the supply chain (base model from HF). Gate 2 checks the artifact: is the merged output structurally safe? Are there code execution payloads, unsafe operators, or format violations?
   - Show: Read `airs/scan_model.py` and display the `detect_source_type()` function (lines 76-88):
     - `gs://` → `GCS`
     - `s3://` → `S3`
     - `https://huggingface.co` → `HUGGING_FACE`
     - Everything else (local paths) → `LOCAL`
   - Then show `resolve_security_group()` (lines 91-138) — how it maps source type to default security group UUID, and the source type mismatch warning.
   - Check: Can the student explain why Gate 1 uses the HF security group (11 rules) and Gate 2 uses LOCAL (7 rules)? What's the conceptual difference between checking the supply chain vs checking the artifact?

3. **Record the Scan in the Manifest**
   - Core idea: Gate 2 already has manifest handling: download Gate 1's manifest (line ~275), set version (line ~286), upload manifest with published model (line ~293). After the scan step, add `manifest.py add-scan` to record the Gate 2 scan result in the manifest. This creates the provenance chain: the manifest documents that this specific model artifact was scanned at Gate 2 with a specific verdict and scan UUID. Gate 3 will verify this record before deploying.
   - Show: Read the existing manifest steps in `gate-2-publish.yaml` (lines 275-303). Point out the flow: Download Manifest → **(scan + add-scan goes HERE)** → Set Version → Upload Manifest. The scan recording fits naturally into the existing manifest pipeline.
   - The command: `python scripts/manifest.py add-scan --manifest manifest.json --gate gate2 --scan-uuid $SCAN_UUID --verdict $VERDICT --security-group $SG_UUID --target "$MODEL_PATH" --target-type merged_model`
   - Check: What will the manifest contain after Gate 2 completes? (lineage from create, Gate 1 scan record, training metadata, Gate 2 scan record, version info)

### Action

1. Add a scan step to `gate-2-publish.yaml` between Merge and Publish:
   - Use Gate 1's scan step as a reference pattern
   - Scan `$MODEL_PATH` (the local merged model directory)
   - Include credentials from secrets, `--output-json`, verdict parsing
   - NO `--warn-only` — strict mode
2. Add `manifest.py add-scan --gate gate2 --scan-uuid $SCAN_UUID --verdict $VERDICT` after the scan step
3. Commit and push
4. Trigger Gate 2 → verify scan runs, manifest is updated, model is published

### Debrief

- Two gates done: Gate 1 checks the supply chain (HF base model, 11 rules with governance), Gate 2 checks the artifact (local merged model, 7 threat detection rules). Different contexts, different security groups, same enforcement mechanism (exit code 1 → step fails → pipeline halts).
- The manifest now has a documented Gate 2 scan record — a provenance trail proving this specific model was scanned before publishing.
- Foreshadow Gate 3: "The model is now published to GCS. Gate 3 deploys it. But between publish and deploy, the model sits in GCS. Should we scan it one more time before putting it on a GPU endpoint serving real users?"

### Deep Dive

For `/lab:explore`: `lab/topics/module-5/00-pipeline-scanning.md`

---

## Challenge 5.3: Gate 3 — Pre-Deploy Scan (GCS Source)

### Learning Objectives

The student should be able to:
- Add scanning to Gate 3 before deployment, completing the third source type (GCS)
- Explain why scanning at deploy time adds defense-in-depth even after Gate 2's scan
- Add manifest verification as a complementary provenance check with a break-glass override

### Key Concepts

Teach these BEFORE modifying the workflow. One at a time, wait for response.

1. **Why Scan Again Before Deploying?**
   - Core idea: The model was scanned in Gate 2 before publishing. Why scan it AGAIN in Gate 3? Defense in depth:
     - The model has been sitting in GCS since Gate 2 published it — it could have been tampered with (unlikely but possible in a shared bucket)
     - Someone could trigger Gate 3 pointing at a model that was never scanned (e.g., a manually-uploaded model, or a model from before scanning was enabled)
     - Gate 3's GCS scan validates the model in its DEPLOYED format, from its PRODUCTION location — not a local runner directory
   - This also completes all three source types: HuggingFace (Gate 1), Local (Gate 2), GCS (Gate 3). Same scanner, three different security groups, three different scanning contexts. The student has now experienced the full source type spectrum.
   - Check: Can the student explain what could go wrong between Gate 2's scan and Gate 3's deploy? Why is "scan once at publish" insufficient for a security-conscious organization?

2. **Adding the Scan to Gate 3**
   - Core idea: Gate 3 resolves the model URI from GCS (the "Resolve Model URI" job, which outputs `$MODEL_URI` — a `gs://` path). The scan goes AFTER model resolution (now we know the GCS path) and BEFORE deployment. The scan target is `$MODEL_URI` (e.g., `gs://syoungberg-airs-lab/approved-models/cloud-security-advisor/v2.0.0`). The SDK detects `gs://` as `GCS` source type and uses the Default GCS security group.
   - Note: For GCS scanning, the SDK automatically downloads the model to the runner using Google Application Default Credentials, scans it locally, then cleans up. The runner needs GCP auth (already configured via Workload Identity Federation) and disk space for the model.
   - Show: Read `.github/workflows/gate-3-deploy.yaml` and display:
     - The "Resolve Model URI" job (lines 148-185) — outputs `model_uri` (a `gs://` path)
     - The "Deploy Model to Vertex AI" job (line 190+) — `needs: [resolve-inputs, resolve-model]`
     - The scan step should go at the START of the "Deploy Model" job (after checkout and GCP auth, before any deployment steps) OR as a standalone job between resolve-model and deploy-model
   - Check: Where should the scan step go? What changes to job dependencies are needed if adding a standalone job?

3. **Manifest Verification — Complementary Provenance Check**
   - Core idea: The Gate 3 scan validates the model is safe RIGHT NOW. Manifest verification validates the model was scanned BEFORE — it has a documented provenance trail. Both are valuable:
     - **Scan:** "Is this model structurally safe at this moment?" (real-time check)
     - **Manifest verify:** "Has this model been through the full pipeline with passing scans?" (provenance check)
   - Add `manifest.py verify --require-scan gate2 --require-verdict ALLOWED` as a step alongside the Gate 3 scan. The manifest was uploaded to GCS alongside the model by Gate 2. Gate 3's existing code already downloads it (line ~462).
   - Add a `skip_manifest_check` workflow dispatch input for break-glass emergencies. When used: requires post-incident review. This is not a convenience bypass — it's an auditable emergency override.
   - Check: Can the student explain the difference between the scan (real-time safety) and manifest verification (provenance)? When would you need one but not the other?

> **ENGAGE**: "You now have three scans: Gate 1 (HuggingFace), Gate 2 (Local), Gate 3 (GCS). Each uses a different security group with different rules. Is this redundant? Or is each scan checking something the others don't?"
> Award 1 pt for meaningful engagement. No wrong answers — teach if needed.
> (Answer: Not redundant — each gate scans at a different point with different context. Gate 1: supply chain check on the external source. Gate 2: artifact check on the merged output. Gate 3: pre-deploy check from the production location. Different source types mean different rule sets — HF has governance rules, LOCAL and GCS have threat detection only. Defense in depth: if any one gate is bypassed or misconfigured, the others still catch issues.)

### Action

1. Add scan step to `gate-3-deploy.yaml`:
   - Scan `$MODEL_URI` (GCS path from the resolve-model job)
   - Include AIRS credentials from secrets
   - Include `--output-json` for reporting
   - NO `--warn-only`
2. Add manifest verification step:
   - Download manifest from `$MODEL_URI/manifest.json` (Gate 3 already has this code — augment it)
   - Run `python scripts/manifest.py verify --manifest manifest.json --require-scan gate2 --require-verdict ALLOWED`
   - Add `skip_manifest_check` input with appropriate conditional logic
3. Commit and push
4. Trigger Gate 3 → verify scan runs, manifest verifies, deployment proceeds

### Debrief

- The pipeline now has end-to-end scanning: supply chain (Gate 1 / HF), artifact (Gate 2 / LOCAL), pre-deploy (Gate 3 / GCS). Three source types, three security groups, three enforcement points.
- Manifest verification adds provenance on top: even if Gate 3's scan passes, the manifest confirms the model went through the full pipeline. Belt AND suspenders.
- The customer story: "Every model in production has been scanned at every stage — before training, after merge, before deployment. Three independent validation points, each with its own security group policy. Plus a documented chain of custody via manifest."

### Deep Dive

For `/lab:explore`: `lab/topics/module-5/01-manifest-verification.md`

---

## Challenge 5.4: Labels & Traceability

### Learning Objectives

The student should be able to:
- Explain why scan labels matter for compliance, incident response, and security operations
- Add label support to `scan_model.py` by exposing the SDK's `labels` parameter
- Apply labels to all three pipeline gates and verify they appear in SCM

### Key Concepts

Teach these BEFORE modifying scan_model.py. One at a time, wait for response.

1. **Why Labels Matter — From Model Cards to Scan Metadata**
   - Core idea: Without labels, a scan is anonymous — you know a model was scanned but not which pipeline run, which version, which environment, which base model. Six months from now, the CISO asks: "Which models were scanned in Q3? Which pipeline run produced this production model?" Without labels, that query requires digging through months of CI/CD logs.
   - Connect to HuggingFace: HF model cards contain metadata about models — license, tags, datasets, base model, training details. AIRS labels serve a similar purpose but for scan records: connecting each scan to its business context. Model cards describe the MODEL. Labels describe the SCAN.
   - Show: If the student has run scans, navigate to SCM → AI Model Security → Scans. Find a scan — it has a verdict and a UUID, but no business context. "Your CISO can't answer 'which models passed scanning this quarter' from this."
   - Useful labels for ML pipelines:

     | Label Key | Value Source | Purpose |
     |-----------|-------------|---------|
     | `gate` | gate1, gate2, gate3 | Which pipeline stage |
     | `run_id` | `$GITHUB_RUN_ID` | Link scan to specific pipeline execution |
     | `model_version` | workflow input | Which version of the model |
     | `environment` | staging, production | Deployment target |
     | `base_model` | Qwen/Qwen2.5-3B-Instruct | Training provenance |

   - Check: Can the student give 3 real scenarios where a security team would need to query scans by label? (Compliance audit, incident investigation, environment-specific reporting)

2. **scan_model.py Doesn't Support Labels Yet — Fix It**
   - Core idea: The AIRS SDK's `scan()` method accepts a `labels` parameter — a dict of key-value string pairs. But the project's `scan_model.py` wrapper doesn't expose this. The argparse section has `--model-path`, `--security-group`, `--warn-only`, `--output-json` — no label argument. The student discovers the gap and fixes it. This is exactly what a consultant would do when implementing AIRS in a customer's pipeline: find a gap in the wrapper, fix it.
   - Show: Read `airs/scan_model.py` — display the argparse section (lines 50-61). No label argument. Then display the `scan_model()` function (lines 141-191) — the `client.scan()` call. Point out that the SDK accepts `labels=` but the wrapper doesn't pass any.
   - To implement:
     - Add `--label` argument to argparse: `parser.add_argument("--label", "-l", action="append", help="Label as key=value (repeatable)")`
     - Parse labels into a dict in `main()`: split each `key=value` string
     - Pass `labels=label_dict` to `client.scan()` call
   - Check: Can the student explain what needs to change? (Three places: argparse definition, label dict construction in main, passing to client.scan)

3. **Verify Labels in SCM**
   - After adding label support and running a labeled scan: navigate to SCM → AI Model Security → Scans → find the scan → verify labels appear on the scan record.
   - This closes the loop: labels go in at scan time → stored with the scan → visible in SCM for querying and filtering.
   - Check: Can the student find their labeled scan in SCM? Can they filter scans by a label value?

### Action

1. Modify `airs/scan_model.py`:
   - Add `--label` / `-l` argument to argparse (repeatable, format: `key=value`)
   - Parse label arguments into a dict: `{k: v for k, v in (l.split("=", 1) for l in args.label)}` if args.label else None
   - Pass `labels=label_dict` to the `client.scan()` call
2. Update all three pipeline scan steps to include labels:
   ```
   --label gate=gate1 --label run_id=$GITHUB_RUN_ID --label base_model=$BASE_MODEL
   --label gate=gate2 --label run_id=$GITHUB_RUN_ID --label model_version=$MODEL_VERSION
   --label gate=gate3 --label run_id=$GITHUB_RUN_ID --label environment=$TARGET_ENV
   ```
3. Commit and push
4. Trigger a pipeline run → navigate to SCM → verify labels appear on the scan records

### Debrief

- Labels transform raw scan data into queryable operational intelligence. Every scan now carries its business context — which gate, which pipeline run, which model version, which environment.
- Connect to the compliance story: scanning (5.1-5.3) + provenance (manifest) + traceability (labels) = a complete, auditable model security program.
- The customer talking point: "Labels make compliance queries possible without digging through CI/CD logs. 'Show me all production scans from Q3' is a one-click filter in SCM."

### Deep Dive

For `/lab:explore`: `lab/topics/module-5/02-scan-labels.md`

---

## Challenge 5.5: Enrich Scan Output for Developers

### Learning Objectives

The student should be able to:
- Surface scan results directly in GitHub Actions job summaries using `$GITHUB_STEP_SUMMARY`
- Explain the SDK's per-rule detail gap and frame it honestly for a customer
- Build a developer-friendly scan report with available data

### Key Concepts

Teach these BEFORE building the summary step. One at a time, wait for response.

1. **The SDK Gap: Aggregate vs Detail**
   - Core idea: The SDK returns `eval_outcome`, `eval_summary` (rules passed/failed counts), `uuid`, and labels. It does NOT return per-rule evaluation details — which specific rule failed, what it found, remediation steps. Those are only available in SCM (or via the data API discovered in Module 4.5). This means: developer triggers pipeline → scan fails → developer sees "AIRS scan: BLOCKED" with an aggregate count but no context → they file a ticket → security team logs into SCM → finds the scan UUID → relays information. This round-trip takes hours.
   - Show: Display a scan response JSON from `--output-json` output. Point out what's there (`eval_outcome`, `eval_summary`, `uuid`, labels, `model_formats`) and what's missing (per-rule details, violation descriptions).
   - Check: Can the student describe the developer experience problem? What would a developer need to see in GitHub Actions to self-serve instead of filing a ticket?

2. **GitHub Actions Step Summary**
   - Core idea: `$GITHUB_STEP_SUMMARY` is a special GitHub Actions file — any markdown written to it renders on the workflow run page as a formatted summary. Write scan results there so developers see a formatted report without leaving GitHub: verdict badge, rule counts, scan UUID (linked to SCM), labels, and a note about where to find per-rule details.
   - Show: Gate 3 already has a basic summary step (writes "Gate 3: Deploy Complete"). Show this as a reference pattern. Then show how to write richer markdown to `$GITHUB_STEP_SUMMARY`.
   - Check: What information should the summary include? (Verdict, rules passed/failed, scan UUID as a link to SCM, labels, timestamp)

> **ENGAGE**: "Per-rule details require SCM access — developers can't see them in CI/CD. How would you frame this limitation to a customer?"
> Award 1 pt for meaningful engagement. No wrong answers — teach if needed.
> (Answer: The honest framing: "Here's what we show in CI/CD today — verdict, rule summary, and a one-click link to full details in SCM. For teams that want per-rule details directly in their CI tool, that's a product enhancement we're actively working on. In the meantime, the SCM link puts full details one click away.")

### Action

1. Add a summary step to the Gate 2 scan workflow (after scanning, reading the JSON output):
   - Read `scan-result.json`
   - Write formatted markdown to `$GITHUB_STEP_SUMMARY`:
     - Verdict badge (ALLOWED ✅ / BLOCKED ❌)
     - Rule summary: X/Y passed, Z/Y failed
     - Scan UUID
     - Labels
     - Link to SCM scan details page
2. Repeat for Gate 1 and Gate 3 scan steps
3. Commit and push
4. Trigger a pipeline run → check the GitHub Actions workflow run page for the formatted summary

### Debrief

- The developer experience is now: pipeline runs → scan results appear directly in GitHub Actions → developers see verdict, context, and a link to SCM for full details. No ticket required for the common case.
- The honest customer framing: aggregate in CI/CD, per-rule in SCM. Bridge the gap with what's available, acknowledge the limitation, flag the feature request.
- Module 5 complete: the pipeline now has end-to-end scanning (3 gates, 3 source types), manifest provenance, scan labels, and developer-friendly reporting.

### Deep Dive

For `/lab:explore`: `lab/topics/module-5/03-evaluations-api.md`

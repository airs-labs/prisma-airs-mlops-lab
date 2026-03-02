# Module 4 Flow: AIRS Deep Dive

> INTERNAL PLAYBOOK — never shown to students.
> Engagement points tracked during module. All other scoring happens during /lab:verify-4.

## Points Available

| Source | Points | When |
|--------|--------|------|
| Engage: Least privilege for CI/CD (4.1) | 1 | During flow |
| Engage: Block vs alert policy (4.5) | 1 | During flow |
| Technical: Deployment profile active | 2 | During verify |
| Technical: Credentials validated | 2 | During verify |
| Technical: Security groups identified | 2 | During verify |
| Technical: SCM reports visible | 2 | During verify |
| Quiz Q1: Source type mismatch | 3 | During verify |
| Quiz Q2: Warning vs blocking | 3 | During verify |
| **Total** | **16** | |

---

## Challenge 4.1: Verify Model Security Activation

### Flow

**Context:** Students created the Model Security deployment profile and kicked off provisioning back in Module 0 (Challenge 0.4). This challenge verifies it's active and credentials work.

> CONTEXT: Read `.claude/reference/airs-provisioning.md` for verification steps.

**Step 1: Verify in SCM**

Navigate to SCM → **Insights** → **Prisma AIRS** → **Model Security** (or **AI Security** → **AI Model Security**). The student should see the Model Security dashboard.

If NOT yet active:
- Check Hub → Common Services → Tenant Management → Deployment Profiles → status
- If still provisioning, have the student continue with 4.2's conceptual content and come back
- If activation failed, troubleshoot (common: wrong TSG, region mismatch)

**Step 2: Re-validate AIRS Credentials**

The student configured GitHub secrets in Module 0. Verify they still work locally:

```bash
# Check environment variables are set (source .env if needed)
source .env 2>/dev/null
echo $AIRS_MS_CLIENT_ID
echo $TSG_ID
```

If credentials are missing locally (only set as GH secrets), have the student source their `.env` file or recreate it from their CSV download.

> **ENGAGE**: "The credentials you're using — do they have admin access or just scanning access? In a real enterprise, what permissions should a CI/CD scanning pipeline have?"
> Award 1 pt for meaningful engagement. No wrong answers — teach if needed.
> (Answer: Scanning-only SA — can submit scans and read results, not manage security groups or users. Least privilege principle.)

---

## Challenge 4.2: Explore the SCM Console

### Flow

**Navigate to AI Model Security in SCM.** The student should explore each area:

**1. Model Security Dashboard** — Overview of recent scan activity, summary statistics.

**2. Scans View** — List of all scans submitted via CLI/SDK. Each shows verdict, UUID, timestamp, security group. Click into a scan for per-rule details (NOT available via SDK — only in SCM).

**3. Security Groups View** — Default security groups pre-created per source type (Local, GCS, S3, Azure, HuggingFace, Artifactory, GitLab). Each bound to a specific Model Source.

**4. Find and Record Default Security Group UUIDs** — The student needs UUIDs for Default Local, Default GCS, and Default Hugging Face.

**Note on `scan_model.py`:** The `SECURITY_GROUPS` dict has placeholder UUIDs. Students can either replace placeholders or pass UUIDs via `--security-group` flag.

**5. Rules View** — Explore available rules: Runtime Code Execution, Load-Time Code Execution, Stored In Approved File Format, Known Malicious Model, License and org validation rules.

### Hints

**Hint 1 (Concept):** SCM is the management plane — where security admins configure policy. The SDK/CLI is the data plane — where scans are submitted and verdicts returned.

**Hint 2 (Approach):** Default security groups use balanced policies — some rules block, others alert. Students will use defaults first, then explore changing enforcement modes.

**Hint 3 (Specific):** The security group UUID connects a scan to a policy. Different UUIDs = different policies = potentially different verdicts for the same model.

---

## Challenge 4.3: Your First Scans

### Flow

Start with the project's scanner wrapper:
```
python airs/scan_model.py --model-path models/test --security-group <their-local-uuid>
```

Once that works, try other scan interfaces: CLI scan, SDK from Python, and examine exit code behavior.

After scanning, verify results appear in SCM → AI Model Security → Scans.

### Hints

**Hint 1 (Concept):** The AIRS SDK is distributed via authenticated PyPI. The package name is `model-security-client`. Check `airs/scan_model.py` to see how this project wraps the SDK.

**Hint 2 (Approach):** Run `python scripts/create_threat_models.py pickle-bomb` to create a malicious model file. AIRS will detect the `os.system` call in the pickle bytecode.

**Hint 3 (Specific):** Clean model → `eval_outcome: ALLOWED` with `rules_failed: 0`. Pickle bomb → `eval_outcome: BLOCKED` (if blocking) or `ALLOWED` with `rules_failed > 0` (if alerting). The difference is policy, not detection.

---

## Challenge 4.4: HuggingFace Integration

### Flow

Explore the HF partnership: public scan badges, what free scans provide vs what AIRS adds.

Questions to answer:
- What does a customer get for free from the HF partnership?
- What does AIRS add beyond free scans?
- When would you recommend AIRS even for HuggingFace-only users?

### Hints

**Hint 1 (Concept):** Free HF scanning gives basic safety checks on public models with default rules.

**Hint 2 (Approach):** AIRS adds: custom policies, blocking enforcement in CI/CD, private model scanning, scan labeling, SCM management, RBAC, and security operations integration.

**Hint 3 (Specific):** Use the Default Hugging Face security group UUID to scan an HF model through your own tenant. Compare results to what HF shows publicly.

---

## Challenge 4.5: Security Groups & Policy

### Flow

Understand source types, enforcement modes, and policy configuration.

1. In SCM, examine a default security group's rules. Toggle between "block" and "alert".
2. Test the effect by scanning the same model before and after changing enforcement.
3. Try a source type mismatch: scan a local model using a GCS security group UUID. Observe the error.

> **ENGAGE**: "When would you configure a security group rule to alert instead of block? Give a real customer scenario."
> Award 1 pt for meaningful engagement. No wrong answers — teach if needed.
> (Answer: Dev/staging environments use warning-only for iteration speed. Production uses strict blocking. Same rules, different enforcement modes.)

### Hints

**Hint 1 (Concept):** Each security group is bound to a source type. This binding is permanent. Rules within can toggle between block and alert independently.

**Hint 2 (Approach):** Enterprise pattern: dev = warning-only, production = strict blocking. Different security groups, same rules, different modes.

**Hint 3 (Specific):** `rules_failed` counts ALL detections. `eval_outcome=BLOCKED` only when a blocking rule detects an issue. Same detection, configurable enforcement — that's the value proposition.

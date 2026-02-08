# Module 4 Flow: AIRS Deep Dive

## Points Available

[to be configured in Phase 4]

---

## Challenge 4.1: Set Up Least-Privilege Access

### Flow (@all)

**Your mission:**
- Create a custom role called `model-scanning-only` with minimum required permissions
- Create a service account called `airs-mlops-lab` assigned that role
- Verify that the SA can scan but cannot administer security groups

**Key questions to explore:**
- What permissions does a scanning pipeline actually need?
- What should it explicitly NOT have access to?
- How would you explain this RBAC setup to a customer running ML pipelines in production?

### Hints

**Hint 1 (Concept):** Ask Claude to use Context7 to fetch the SCM API docs for IAM. The key question is: what permissions exist for AI Model Security? Start by understanding the permissions model before creating anything.

**Hint 2 (Approach):** SCM exposes IAM operations through its REST API. You need to explore: custom role creation, service account creation, and role assignment. Claude can interact with these APIs directly -- you are building an agent-driven RBAC workflow.

**Hint 3 (Specific):** After creating the restricted SA, verify it works by running a scan. Then verify it is restricted by attempting an admin operation (like creating a security group). The scan should succeed. The admin operation should fail with a permissions error.

### Points: 0

---

## Challenge 4.2: Your First Scans

### Flow (@all)

**What to examine in the scan response:**
- `uuid` -- the unique identifier for this scan (used for lookups and evaluations)
- `eval_outcome` -- the verdict: ALLOWED, BLOCKED, PENDING, or ERROR (these are the only four values that exist)
- `eval_summary` -- aggregate counts of what passed and what failed
- `rules_passed` / `rules_failed` -- how many rules detected issues

**What to try:**
1. CLI scan: `model-security scan --security-group-uuid "..." --model-uri "..."`
2. SDK scan from Python (reference `scripts/test_airs_sdk.py`)
3. CLI exit code behavior: what does exit code 0 mean vs exit code 1?

### Hints

**Hint 1 (Concept):** The AIRS SDK is distributed via an authenticated PyPI installation. The package name is `model-security-client`. After installation, you get both the Python SDK and the `model-security` CLI tool. Check `airs/scan_model.py` to see how this project wraps the SDK.

**Hint 2 (Approach):** Run `python scripts/create_threat_models.py pickle-bomb` to create a malicious model file. The payload is safe -- it only writes a marker file. But AIRS will detect the `os.system` call embedded in the pickle bytecode and flag it.

**Hint 3 (Specific):** The clean model should return `eval_outcome: ALLOWED` with `rules_failed: 0`. The pickle bomb should return `eval_outcome: BLOCKED` (if using a blocking security group) or `eval_outcome: ALLOWED` with `rules_failed > 0` (if using a warning-only group). The difference is the security group policy, not the detection itself.

### Points: 0

---

## Challenge 4.3: HuggingFace Integration

### Flow (@all)

**What to explore:**
- Visit HuggingFace model pages and look for PANW security scan badges
- Compare the public scan output to what the full AIRS SDK returns
- HF-specific evaluations: verified organizations, license compliance, model blocked status

**Questions to answer:**
- What does a customer get for free from the HF partnership?
- What does a customer get from AIRS that they cannot get from the free scans?
- When would you recommend a customer use AIRS even if they only use HuggingFace models?

### Hints

**Hint 1 (Concept):** Browse popular model pages on HuggingFace. Look for security or safety badges. Palo Alto scans public models and makes basic results available. The key is understanding the scope: public scans cover publicly hosted models with default policies.

**Hint 2 (Approach):** Free HF scanning gives you: basic safety checks on public models with default rules. AIRS adds: custom security policies, blocking enforcement in CI/CD, private model scanning, scan labeling, SCM management, RBAC, and integration with your security operations workflow. The customer question is not "do I need scanning?" but "do I need control over my scanning policy?"

**Hint 3 (Specific):** This project has a HuggingFace security group: `00000000-0000-0000-0000-000000000003`. You can scan HF models through AIRS with your own policy. Compare the results to what HF shows publicly. The depth of evaluation data is the differentiator.

### Points: 0

---

## Challenge 4.4: Security Groups Deep Dive

### Flow (@all)

**What to understand:**
- Source types: LOCAL, GCS, HUGGING_FACE, S3, AZURE_BLOB
- Each security group is bound to a source type
- The source type of the security group MUST match the model being scanned
- Default security groups exist per source type and are used when no UUID is specified
- Groups are selected by UUID -- the SDK enforces source type matching

**What to build:**
1. Navigate to SCM: AI Security -> AI Model Security -> Scans (find your reports)
2. Create a custom security group: "Lab - Blocking All" with every rule set to block
3. Create another: "Lab - Warning Only" with every rule set to alert/warn
4. Scan the same model (e.g., the pickle bomb) against both groups
5. Compare: same model, same rules detecting the same issue, but BLOCKED vs ALLOWED

**Research questions to investigate with Claude:**
- What happens if you scan a GCS model with a LOCAL security group?
- When would you set evaluations to warn instead of block?
- How does source type matching work exactly?

### Hints

**Hint 1 (Concept):** In SCM, navigate to AI Security, then AI Model Security, then Scans. Your CLI scans from Challenge 4.2 should appear here. Click into a scan to see per-rule evaluations and what each rule detected.

**Hint 2 (Approach):** In SCM, navigate to Security Groups under AI Model Security. When creating a new group, you must select a source type. For testing with local models, choose LOCAL. For GCS models, choose GCS. Each rule can be set to "block" or "alert" (warn) independently.

**Hint 3 (Specific):** `rules_failed` counts ALL rules that detected issues -- blocking and non-blocking. `eval_outcome=BLOCKED` only occurs when a rule with Blocking=On detects an issue. The same detection, the same rule, produces different outcomes based on policy. This is the core value proposition: detection is the same, enforcement is configurable.

### Points: 0

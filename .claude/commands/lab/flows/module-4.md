# Module 4 Flow: AIRS Deep Dive

## Points Available

| Source | Points | Track |
|--------|--------|-------|
| Deployment profile active in SCM | 2 | @all |
| AIRS credentials validated (scan succeeds) | 2 | @all |
| Default security groups identified in SCM | 2 | @all |
| SCM scan reports visible | 2 | @all |
| Understanding: source type mismatch | 3 | @all |
| Understanding: warning vs blocking scenario | 3 | @all |
| **Total** | **14** | |

---

## Challenge 4.1: Activate AI Model Security

### Flow (@all)

**Context:** Students already have a Prisma AIRS tenant from a previous AIRS API Lab. That tenant has SCM provisioned. Now they need to add the AI Model Security capability to that same tenant.

**Step 1: Create a Deployment Profile in the Customer Support Portal (CSP)**

Walk the student through this process. They need to:

1. Log in to CSP (https://support.paloaltonetworks.com)
2. Navigate to **Products** → **Software/Cloud NGFW Credits**
3. Locate their credit pool and click **Create Deployment Profile**
4. Under **Select firewall type**, expand **Prisma AIRS** and select **Model Scanning (preview)**
5. Configure the deployment (regions, scan allocation)
6. Click **Create Deployment Profile**

**Step 2: Associate to Their Existing Tenant**

This is critical — they should NOT create a new tenant. They need to associate the deployment profile with the SAME tenant (TSG) they used for the AIRS API Lab.

1. In CSP, find the new deployment profile and click **Finish Setup** → redirects to Hub
2. Select the existing CSP account
3. Select their existing tenant (NOT "create new tenant")
4. Select the deployment profile to associate
5. Agree to terms and click **Activate**

**Important:** Deployment profile activation can take up to 2 hours. If it is not yet active, note this and have the student continue with conceptual exploration. Come back to verify later.

**Step 3: Verify in SCM**

Once activated, navigate to SCM → **Insights** → **Prisma AIRS** → **Model Security** (or **AI Security** → **AI Model Security**). The student should see the Model Security dashboard.

**Step 4: Re-validate AIRS Credentials**

The student configured GitHub secrets in Module 0. Verify they still work locally:

```bash
# Check environment variables are set
echo $MODEL_SECURITY_CLIENT_ID
echo $TSG_ID

# Quick validation — attempt a scan (will also test in 4.2)
python airs/scan_model.py --model-path models/test --warn-only
```

If credentials are missing locally (only set as GH secrets), have the student create a `.env` file for local testing:

```bash
# Create .env for local SDK use (already in .gitignore)
cat > .env << 'EOF'
MODEL_SECURITY_CLIENT_ID=<their-id>
MODEL_SECURITY_CLIENT_SECRET=<their-secret>
TSG_ID=<their-tsg>
EOF
```

**Discussion point — Least Privilege:** Ask the student: "The credentials you're using — do they have admin access or just scanning access? In a real enterprise deployment, what permissions should a CI/CD scanning pipeline have?" This plants the RBAC seed without requiring a full API-driven custom role exercise. Reference the concept: scanning-only SA should be able to submit scans and read results, not manage security groups or users.

### Hints

**Hint 1 (Concept):** AI Model Security is a separate capability from the AIRS API Runtime you used before. It requires its own deployment profile — think of it like enabling a new feature module on your existing platform tenant. The deployment profile is how licensing and feature activation work across all Prisma AIRS products.

**Hint 2 (Approach):** The key decision is step 2 — associating to an EXISTING tenant, not creating a new one. If the student creates a new tenant, they will lose access to their existing SCM configuration and will need to re-provision. Ask them to identify their current tenant name/ID before starting.

**Hint 3 (Specific):** If activation is pending, the student can still explore SCM and work on conceptual understanding. The Model Security UX will appear once activation completes. In the meantime, have them explore the IAM settings (Common Services → Identity & Access) to understand the permissions model for AI Model Security.

### Points: 0

---

## Challenge 4.2: Explore the SCM Console

### Flow (@all)

**Navigate to AI Model Security in SCM.** The student should explore each area:

**1. Model Security Dashboard**
Navigate to: AI Security → AI Model Security (or Insights → Prisma AIRS → Model Security)

What to observe:
- Overview of recent scan activity
- Summary statistics (scans, detections, verdicts)

**2. Scans View**
Navigate to: AI Model Security → Scans

What to observe:
- List of all scans submitted via CLI/SDK
- Each scan shows: verdict (ALLOWED/BLOCKED), scan UUID, timestamp, security group used
- Click into a scan to see per-rule evaluation details (this is the information NOT available via the SDK — only in SCM)

**3. Security Groups View**
Navigate to: AI Model Security → Model Security Groups

What to observe:
- **Default security groups** are pre-created — one per source type (Local, GCS, S3, Azure, HuggingFace, Artifactory, GitLab)
- Each group is bound to a specific Model Source
- Click into a group to see the rules and their enforcement mode (block vs alert/warn)

**4. Find and Record Default Security Group UUIDs**

This is important for the rest of the lab. The student needs to find the UUIDs for:
- **Default Local** — for scanning local model files
- **Default GCS** — for scanning models in Google Cloud Storage
- **Default Hugging Face** — for scanning HuggingFace models

Ask the student: "Where do you see the UUID for each security group?" It should be visible in the group details or the URL when viewing a group.

**Note on `scan_model.py`:** The project's `airs/scan_model.py` has a `SECURITY_GROUPS` dict with placeholder UUIDs. These placeholders need to be replaced with the student's actual security group UUIDs from their tenant, OR students can pass UUIDs directly via the `--security-group` CLI flag. Discuss which approach is better for a pipeline (hardcoded in config vs passed as parameter).

**5. Rules View**
Explore the rules available in a security group:
- Runtime Code Execution (detects pickle `__reduce__` exploits)
- Load-Time Code Execution (detects Keras Lambda layers)
- Stored In Approved File Format (flags non-safetensors formats)
- Known Malicious Model (matches against threat intelligence)
- License validation rules (HuggingFace-specific)
- Verified organization rules (HuggingFace-specific)

Ask: "Which of these rules can you toggle between 'block' and 'alert'? What is the difference?"

### Hints

**Hint 1 (Concept):** SCM is the management plane — where security admins configure policy. The SDK/CLI is the data plane — where scans are submitted and verdicts returned. A security team manages policy in SCM; the CI/CD pipeline calls the SDK. They never need to touch each other's tools.

**Hint 2 (Approach):** The default security groups use balanced policies — some rules block, others alert. For the lab, students will use these defaults first, then explore changing enforcement modes to see how it affects scan outcomes in Challenge 4.4.

**Hint 3 (Specific):** The security group UUID is the single piece of configuration that connects a scan to a policy. When you call `client.scan(security_group_uuid=...)`, you are saying "evaluate this model against THESE rules with THESE enforcement settings." Different UUIDs = different policies = potentially different verdicts for the same model.

### Points: 0

---

## Challenge 4.3: Your First Scans

### Flow (@all)

**What to examine in the scan response:**
- `uuid` -- the unique identifier for this scan (used for lookups and evaluations)
- `eval_outcome` -- the verdict: ALLOWED, BLOCKED, PENDING, or ERROR (these are the only four values that exist)
- `eval_summary` -- aggregate counts of what passed and what failed
- `rules_passed` / `rules_failed` -- how many rules detected issues

**What to try:**
1. CLI scan: `model-security scan --security-group-uuid "..." --model-uri "..."`
2. SDK scan from Python (reference `scripts/test_airs_sdk.py`)
3. Our wrapper: `python airs/scan_model.py --model-path <path> --security-group <uuid-or-shorthand>`
4. CLI exit code behavior: what does exit code 0 mean vs exit code 1?

**Important:** Use the actual security group UUIDs discovered in Challenge 4.2. If the student has not updated `scan_model.py` SECURITY_GROUPS dict, they should pass UUIDs directly:
```
python airs/scan_model.py --model-path models/test --security-group <their-local-uuid>
```

**After scanning, verify in SCM:** Navigate back to AI Model Security → Scans. The scan they just ran should appear. Click into it to see per-rule details.

### Hints

**Hint 1 (Concept):** The AIRS SDK is distributed via an authenticated PyPI installation. The package name is `model-security-client`. After installation, you get both the Python SDK and the `model-security` CLI tool. Check `airs/scan_model.py` to see how this project wraps the SDK.

**Hint 2 (Approach):** Run `python scripts/create_threat_models.py pickle-bomb` to create a malicious model file. The payload is safe -- it only writes a marker file. But AIRS will detect the `os.system` call embedded in the pickle bytecode and flag it.

**Hint 3 (Specific):** The clean model should return `eval_outcome: ALLOWED` with `rules_failed: 0`. The pickle bomb should return `eval_outcome: BLOCKED` (if the security group has Runtime Code Execution set to block) or `eval_outcome: ALLOWED` with `rules_failed > 0` (if set to alert). The difference is the security group policy, not the detection itself.

### Points: 0

---

## Challenge 4.4: HuggingFace Integration

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

**Hint 3 (Specific):** Use the Default Hugging Face security group UUID from Challenge 4.2 to scan a HF model through your own AIRS tenant. Compare the results to what HF shows publicly. The depth of evaluation data and the policy control are the differentiators.

### Points: 0

---

## Challenge 4.5: Security Groups & Policy

### Flow (@all)

**What to understand:**
- Source types: LOCAL, GCS, HUGGING_FACE, S3, AZURE_BLOB, ARTIFACTORY, GITLAB
- Each security group is bound to a source type — this binding is permanent
- The source type of the security group MUST match the model being scanned
- Default security groups exist per source type (auto-created with the deployment profile)
- Rules within a group can be toggled between "block" and "alert" independently

**What to explore:**

1. **In SCM**, open a default security group and examine the rules. Toggle a rule between "block" and "alert" to understand the enforcement options.

2. **Test the effect:** Scan the same model (e.g., the pickle bomb from 4.3) before and after changing a rule's enforcement mode. Observe how `eval_outcome` changes while `rules_failed` stays the same — the detection is identical, only the enforcement differs.

3. **If custom security groups can be created in your tenant:** Create "Lab - Blocking All" with every rule set to block, and "Lab - Warning Only" with every rule set to alert. Scan the same model against both. If custom creation is not available, modify the default group's rules to test both modes.

4. **Source type mismatch:** Try scanning a local model file using a GCS security group UUID (or vice versa). Observe the error. Why does the SDK enforce this?

**Research questions to investigate with Claude:**
- What happens if you scan a GCS model with a LOCAL security group?
- When would you set evaluations to warn instead of block?
- How does source type matching work exactly?
- What enterprise policy would you recommend: one group for all environments, or separate groups per environment?

### Hints

**Hint 1 (Concept):** In SCM, navigate to Security Groups under AI Model Security. Each group shows its bound source type and the list of rules with their current enforcement setting. Clicking into a rule shows what it checks and lets you toggle between "block" and "alert."

**Hint 2 (Approach):** The pattern for an enterprise is: development and staging environments use warning-only policies (detect but don't block), while production uses strict blocking. This lets dev teams iterate without friction while ensuring production is protected. In AIRS, this maps to different security groups with different enforcement settings — same rules, different modes.

**Hint 3 (Specific):** `rules_failed` counts ALL rules that detected issues — blocking and non-blocking. `eval_outcome=BLOCKED` only occurs when a rule with Blocking=On detects an issue. The same detection, the same rule, produces different outcomes based on policy. This is the core value proposition: detection is the same, enforcement is configurable.

### Points: 0

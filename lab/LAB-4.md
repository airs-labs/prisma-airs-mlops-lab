# Module 4: AIRS Deep Dive

## Overview

Welcome to Act 2 -- **Understand the Security.**

You have a working ML pipeline. Models train, merge, publish, and deploy. But right now there is nothing stopping a compromised model from flowing straight to production. Before you can secure the pipeline, you need to understand AIRS inside and out -- the way you would need to demo it to a customer.

This module puts you in the seat of someone evaluating AIRS for an enterprise deployment. You will set up least-privilege access, run your first scans, explore the HuggingFace partnership, and build custom security policies in Strata Cloud Manager.

## Objectives

- Create a restricted service account with minimum scanning permissions (RBAC)
- Install the AIRS SDK and run scans from the CLI and Python
- Understand scan responses: eval_outcome, eval_summary, rules_passed, rules_failed
- Explore the PANW-HuggingFace partnership and compare public vs enterprise scanning
- Navigate Strata Cloud Manager (SCM) to find scan reports and manage security groups
- Create custom security groups with different blocking policies

## Prerequisites

- Modules 0-3 completed (working pipeline, deployed model)
- Access to your Prisma AIRS tenant (SCM credentials)
- AIRS SDK credentials: `MODEL_SECURITY_CLIENT_ID`, `MODEL_SECURITY_CLIENT_SECRET`, `TSG_ID`
- GitHub secrets configured from Module 0

## Time Estimate

1 to 1.5 hours

---

## Challenges

### Challenge 4.1: Set Up Least-Privilege Access

> `/lab:explore 01-rbac`

**The scenario:** Your security team requires that every automated system follows the principle of least privilege. The scanning pipeline should only be able to submit scans and read results -- it should never be able to create or modify security groups, manage users, or change policies.

**Your task:** Use Claude Code and the SCM API to create a custom role that only allows model scanning operations. Create a service account with that role. You will use this restricted service account for all your scanning work in Modules 4 through 7.

**What to build:**
- A custom role called `model-scanning-only` with minimum required permissions
- A service account called `airs-mlops-lab` assigned that role
- Verification that the SA can scan but cannot administer security groups

**Think about:**
- What permissions does a scanning pipeline actually need?
- What should it explicitly NOT have access to?
- How would you explain this RBAC setup to a customer running ML pipelines in production?

<details>
<summary>Hint 1: Where to start</summary>

Ask Claude to use Context7 to fetch the SCM API docs for IAM. The key question is: what permissions exist for AI Model Security? Start by understanding the permissions model before creating anything.
</details>

<details>
<summary>Hint 2: The API approach</summary>

SCM exposes IAM operations through its REST API. You need to explore: custom role creation, service account creation, and role assignment. Claude can interact with these APIs directly -- you are building an agent-driven RBAC workflow.
</details>

<details>
<summary>Hint 3: Testing the restriction</summary>

After creating the restricted SA, verify it works by running a scan. Then verify it is restricted by attempting an admin operation (like creating a security group). The scan should succeed. The admin operation should fail with a permissions error.
</details>

---

### Challenge 4.2: Your First Scans

> `/lab:explore 02-cli-and-sdk`

**The scenario:** A customer asks you to demonstrate AIRS scanning. They want to see what happens with a legitimate model and what happens when something dangerous comes through.

**Your task:** Install the AIRS SDK and run your first scan. Scan a known-safe model from HuggingFace or GCS. Then scan the pickle bomb from `scripts/create_threat_models.py`. Compare the results side by side.

**What to examine in the scan response:**
- `uuid` -- the unique identifier for this scan (used for lookups and evaluations)
- `eval_outcome` -- the verdict: ALLOWED, BLOCKED, PENDING, or ERROR (these are the only four values that exist)
- `eval_summary` -- aggregate counts of what passed and what failed
- `rules_passed` / `rules_failed` -- how many rules detected issues

**What to try:**
1. CLI scan: `model-security scan --security-group-uuid "..." --model-uri "..."`
2. SDK scan from Python (reference `scripts/test_airs_sdk.py`)
3. CLI exit code behavior: what does exit code 0 mean vs exit code 1?

<details>
<summary>Hint 1: SDK installation</summary>

The AIRS SDK is distributed via an authenticated PyPI installation. The package name is `model-security-client`. After installation, you get both the Python SDK and the `model-security` CLI tool. Check `airs/scan_model.py` to see how this project wraps the SDK.
</details>

<details>
<summary>Hint 2: Generating the pickle bomb</summary>

Run `python scripts/create_threat_models.py pickle-bomb` to create a malicious model file. The payload is safe -- it only writes a marker file. But AIRS will detect the `os.system` call embedded in the pickle bytecode and flag it.
</details>

<details>
<summary>Hint 3: Comparing results</summary>

The clean model should return `eval_outcome: ALLOWED` with `rules_failed: 0`. The pickle bomb should return `eval_outcome: BLOCKED` (if using a blocking security group) or `eval_outcome: ALLOWED` with `rules_failed > 0` (if using a warning-only group). The difference is the security group policy, not the detection itself.
</details>

---

### Challenge 4.3: HuggingFace Integration

> `/lab:explore 03-hf-integration`

**The scenario:** A customer tells you, "HuggingFace already scans models. Why do I need AIRS?" You need to understand exactly what the PANW-HuggingFace partnership provides for free, and what AIRS adds on top.

**Your task:** Find Palo Alto Networks' public scan results on HuggingFace. What models have been flagged? What information is freely available vs what AIRS adds for enterprise customers?

**What to explore:**
- Visit HuggingFace model pages and look for PANW security scan badges
- Compare the public scan output to what the full AIRS SDK returns
- HF-specific evaluations: verified organizations, license compliance, model blocked status

**Questions to answer:**
- What does a customer get for free from the HF partnership?
- What does a customer get from AIRS that they cannot get from the free scans?
- When would you recommend a customer use AIRS even if they only use HuggingFace models?

<details>
<summary>Hint 1: Where to look on HuggingFace</summary>

Browse popular model pages on HuggingFace. Look for security or safety badges. Palo Alto scans public models and makes basic results available. The key is understanding the scope: public scans cover publicly hosted models with default policies.
</details>

<details>
<summary>Hint 2: The value proposition</summary>

Free HF scanning gives you: basic safety checks on public models with default rules. AIRS adds: custom security policies, blocking enforcement in CI/CD, private model scanning, scan labeling, SCM management, RBAC, and integration with your security operations workflow. The customer question is not "do I need scanning?" but "do I need control over my scanning policy?"
</details>

<details>
<summary>Hint 3: The source type connection</summary>

This project has a HuggingFace security group: `00000000-0000-0000-0000-000000000003`. You can scan HF models through AIRS with your own policy. Compare the results to what HF shows publicly. The depth of evaluation data is the differentiator.
</details>

---

### Challenge 4.4: Security Groups Deep Dive

> `/lab:explore 04-security-groups`

**The scenario:** An enterprise customer wants different scanning policies for different environments. Development teams should get warnings so they can iterate quickly. Production deployments should be strictly blocked if anything is detected. They also want to understand exactly what each rule does.

**Your task:** Navigate SCM. Find your scan reports from the CLI experiments. Then create two custom security groups: one that blocks on every rule, and one that only warns. Test both against the same model and compare the results.

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

<details>
<summary>Hint 1: Finding your scan reports</summary>

In SCM, navigate to AI Security, then AI Model Security, then Scans. Your CLI scans from Challenge 4.2 should appear here. Click into a scan to see per-rule evaluations and what each rule detected.
</details>

<details>
<summary>Hint 2: Creating security groups</summary>

In SCM, navigate to Security Groups under AI Model Security. When creating a new group, you must select a source type. For testing with local models, choose LOCAL. For GCS models, choose GCS. Each rule can be set to "block" or "alert" (warn) independently.
</details>

<details>
<summary>Hint 3: The key insight</summary>

`rules_failed` counts ALL rules that detected issues -- blocking and non-blocking. `eval_outcome=BLOCKED` only occurs when a rule with Blocking=On detects an issue. The same detection, the same rule, produces different outcomes based on policy. This is the core value proposition: detection is the same, enforcement is configurable.
</details>

---

## Verification

By the end of this module, confirm:

- [ ] Custom role `model-scanning-only` created in SCM with minimum permissions
- [ ] Service account `airs-mlops-lab` created and assigned the restricted role
- [ ] Restricted SA can submit scans successfully
- [ ] Restricted SA cannot perform admin operations (security group management)
- [ ] At least one clean model scanned (ALLOWED result)
- [ ] Pickle bomb scanned (BLOCKED or rules_failed > 0)
- [ ] Can explain the four eval_outcome values: ALLOWED, BLOCKED, PENDING, ERROR
- [ ] Visited HuggingFace and found PANW public scan results
- [ ] Can articulate the difference between free HF scanning and enterprise AIRS
- [ ] Two custom security groups created in SCM (blocking and warning)
- [ ] Same model scanned against both groups with different outcomes
- [ ] Scan reports visible in SCM from CLI experiments
- [ ] Can explain source type matching rules

## Customer Talking Points

After completing this module, you should be able to confidently deliver these points:

**On RBAC:** "Here is how to set up least-privilege access for your scanning pipeline. Your CI/CD runner only needs scan permissions, not admin. This follows the same IAM model you use for every other cloud service."

**On HuggingFace:** "When a customer asks about HF scanning vs AIRS, here is the comparison: HF gives you basic checks on public models with default rules. AIRS gives you policy control, private model scanning, pipeline enforcement, and security operations integration. The question is whether you need visibility or control."

**On Security Groups:** "Different environments need different policies. Development gets warnings so teams can iterate. Staging gets mixed policies for testing. Production gets strict blocking. AIRS makes this a configuration decision, not a code change."

## What's Next

You now understand AIRS scanning inside and out. In Module 5, you will integrate this into your pipeline -- adding scanning gates, manifest verification, and evaluation reporting directly into your GitHub Actions workflows. The pipeline currently has no security checks. You are about to change that.

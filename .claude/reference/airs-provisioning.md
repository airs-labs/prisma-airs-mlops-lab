# AIRS Model Security Provisioning

Step-by-step reference for provisioning AI Model Security. Flow files reference this via `> CONTEXT:` markers. Do NOT dump this on the student — use it to inform your guidance. Point students to techdocs for detailed steps rather than spelling everything out.

## Techdocs References

- Deployment Profile: https://docs.paloaltonetworks.com/ai-runtime-security/ai-model-security/model-security-to-secure-your-ai-models/get-started-with-ai-model-security/create-a-deployment-profile-for-prisma-airs-ai-model-security
- IAM: https://docs.paloaltonetworks.com/ai-runtime-security/ai-model-security/model-security-to-secure-your-ai-models/get-started-with-ai-model-security/configure-identity-and-access-management

## Hub Direct Links

- Tenant Management: https://apps.paloaltonetworks.com/hub/settings/tenants
- IAM / Access Management: https://apps.paloaltonetworks.com/hub/settings/iam/access

---

## Overview: Provisioning Flow

The order depends on whether the student already has a TSG from a prereq lab.

**Has existing TSG (from prereq lab):**
1. Create deployment profile in CSP
2. Finish Setup → associate to existing TSG
3. Create SA in Hub IAM

**No existing TSG (starting fresh):**
1. Create TSG first (Hub → Tenant Management)
2. Create deployment profile in CSP
3. Finish Setup → associate to new TSG
4. Create SA in Hub IAM

---

## Step 1: Create TSG (if needed)

If the student doesn't have a TSG from a prereq lab, create one first.

- **Hub → Common Services → Tenant Management** (https://apps.paloaltonetworks.com/hub/settings/tenants)
- Create a new tenant under the appropriate parent
  - **Workshop scenario:** Create under the workshop parent TSG (e.g., "AIRS Workshop (Technical Services)")
  - **Self-paced / own CSP:** Can use their own existing TSG or create a new one
- Name: something descriptive (e.g., `<username>-api` or `<username>-airs`)
- Creating a new TSG triggers SCM + SLS provisioning: **15-30 minutes**

If the student already has a TSG, skip to Step 2.

## Step 2: Create Deployment Profile in CSP

1. Log in to the Customer Support Portal (CSP): https://support.paloaltonetworks.com
   - Workshop CSP account: 1850598 - Palo Alto Networks - CoE
2. Navigate to **Products → Software/Cloud NGFW Credits**
3. Locate the credit pool → **Create Deployment Profile**
4. Select: **Prisma AIRS → Model Security** → Next
5. Enter a **Profile Name**, click **Calculate Estimated Cost** (1500 credits flat post-GA)
6. **Create Deployment Profile**

## Step 3: Associate Profile to TSG

1. In CSP, find the new profile → click **Finish Setup** → redirects to Hub
2. Select the CSP account
3. Select the **existing tenant** (from Step 1 or prereq lab) — do NOT create a new one here
4. **Region:** United States - Americas (only region supported currently)
5. Select the Model Security deployment profile
6. Additional Services: **None**
7. Agree to terms → **Activate**

If SCM is already provisioned on this TSG (from prereq lab), activation is near-instant.
If new TSG, this triggers provisioning: student can continue with Modules 1-3 while it completes.

### Common Mistakes

- **Creating a new tenant when they already have one** — orphans the SCM instance, wastes credits
- **Wrong CSP account selected** — profile goes to wrong credit pool
- **Forgetting to click "Finish Setup"** — profile created but never associated, never activates

## Step 4: Verify Activation

Two ways to verify:

1. **Hub → Tenant Management** → select tenant → **Deployment Profiles** tab → status "Complete"
2. **SCM → Insights → Prisma AIRS → Model Security** — dashboard visible with scan activity area

Activation can take up to 2 hours per techdocs. Usually faster (minutes to 30 min).

---

## Step 5: Configure IAM & Create Service Account

**Hub → Identity & Access → Access Management** (https://apps.paloaltonetworks.com/hub/settings/iam/access)

Select your TSG first, then configure roles and service accounts.

### Step 5a: Create Custom Role (for reference — see Known Issue)

Per techdocs, the intended flow is:
1. Select your TSG in the IAM access panel
2. **Roles** tab → **Custom Roles** → **Add Custom Role**
3. Name and describe the role
4. Enable **AI Model Scanning** permissions — the UI shows granular permissions including:
   - `ai_ms.pypi_auth` — SDK authentication / PyPI access
   - `ai_ms.scans` — submit and read scans
   - `ai_ms.security_groups` — manage security groups
   - `ai_ms.evaluations`, `ai_ms.files`, `ai_ms.rule_instances`, `ai_ms.scan_labels` — additional granular permissions
5. Save the role

For full details, refer students to the techdocs IAM page.

### Step 5b: Create Service Account

1. Still in Hub IAM → select your TSG
2. **Service Accounts** → create new
3. Name: descriptive (e.g., `mlops-lab-scanner`)
4. **Assign Role:** **Superuser** (see Known Issue below)
5. **Download the credentials immediately** — CLIENT_ID and CLIENT_SECRET
   - Cannot retrieve the secret later. If lost, create a new SA.
6. Note the **TSG_ID** from Tenant Management (select tenant → TSG ID shown at top)

The SA is automatically scoped to the TSG you're managing when you create it.

### Known Issue: Custom Roles Return 403 (as of March 2026)

**Bug:** Custom roles with AI Model Scanning permissions return HTTP 403 on all AIRS API endpoints, even when permissions are correctly enabled in the UI. Only the **Superuser** built-in role works reliably.

Until resolved, use **Superuser** for the lab SA.

**Teaching point:** AIRS has granular IAM — the UI lets you create fine-grained roles with specific API permissions. The design is right (least-privilege, separation of duties), but the enforcement has a bug post-GA. For customer conversations:
- The architecture supports least-privilege — that's the selling point
- Use Superuser for POCs/labs while the fix ships
- If a customer hits this in production, flag it with your SE

---

## How PyPI Authentication Works

The AIRS Model Security SDK is distributed via a private PyPI repository hosted on Google Artifact Registry. To install it, the pipeline needs an authenticated PyPI URL:

1. **OAuth token**: SA credentials → `auth.apps.paloaltonetworks.com/oauth2/access_token` → bearer token
2. **PyPI URL**: Bearer token → `api.sase.paloaltonetworks.com/aims/mgmt/v1/pypi/authenticate` → time-limited PyPI URL with embedded credentials
3. **pip install**: `pip install --extra-index-url "$PYPI_URL" aimsdk` → installs from the private repo

The `scripts/get-pypi-url.sh` script handles steps 1-2. If the SA doesn't have the right permissions (or the RBAC bug triggers), step 2 fails with 403.

---

## Relationship: Deployment Profiles ↔ TSGs ↔ SCM

```
CSP Account (credit pool)
  └─ Deployment Profile (Model Security, 1500 credits)
       └─ Associated to TSG
            └─ SCM Instance (auto-provisioned if needed)
                 ├─ Model Security dashboard
                 ├─ Security Groups (auto-created defaults)
                 ├─ Service Accounts (you create via Hub IAM)
                 └─ Scan history
```

- One TSG can have multiple deployment profiles (Model Security + Runtime + Red Team)
- Each deployment profile consumes credits independently
- SCM is provisioned once per TSG — subsequent profiles just add features

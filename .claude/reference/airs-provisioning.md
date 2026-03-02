# AIRS Model Security Provisioning

Step-by-step reference for provisioning AI Model Security. Flow files reference this via `> CONTEXT:` markers. Do NOT dump this on the student — use it to inform your guidance.

## Techdocs Reference

https://docs.paloaltonetworks.com/ai-runtime-security/ai-model-security/model-security-to-secure-your-ai-models/get-started-with-ai-model-security/create-a-deployment-profile-for-prisma-airs-ai-model-security

## Step 1: Create Deployment Profile in CSP

1. Log in to the Palo Alto Networks Customer Support Portal (CSP)
   - URL: https://support.paloaltonetworks.com
   - Workshop CSP account: 1850598 - Palo Alto Networks - CoE
2. Navigate to **Products** → **Software/Cloud NGFW Credits**
3. Locate the credit pool and click **Create Deployment Profile**
4. Under **Select firewall type**, expand **Prisma AIRS** and select **Model Security**
5. Click **Next**
6. Enter a **Profile Name** (recommend: `<username>-model-security`)
7. Click **Calculate Estimated Cost** to view credit consumption (1500 credits flat post-GA)
8. Click **Create Deployment Profile**

## Step 2: Associate to Tenant (TSG)

**Critical decision: existing vs new tenant.**

### Option A: Associate to Existing TSG (Ideal)

If the student already has a TSG from the n8n prereq lab:

1. In CSP, find the new deployment profile → click **Finish Setup** → redirects to Hub
2. Select the CSP account name
3. Select their **existing tenant** (e.g., `<username>-api`)
4. **Region:** United States - Americas (only supported currently)
5. Select the Model Security deployment profile
6. Select **None** for Additional Services
7. Agree to terms → **Activate**

If SCM is already provisioned on this TSG → activation is near-instant.

### Option B: Create New TSG

If the student doesn't have an existing TSG:

1. Same flow as Option A, but at step 3: click **+** to create new sub-tenant
2. Name: `<username>-model-security` (or similar)
3. Nest under the parent TSG (workshop: "AIRS Workshop")
4. This triggers SCM + SLS provisioning: **15-60 minutes**
5. Student should continue with Modules 1-3 while provisioning completes

### Common Mistakes

- **Creating a new tenant when they already have one** — orphans the new SCM instance, wastes credits
- **Wrong CSP account selected** — profile goes to wrong credit pool
- **Region mismatch** — only US-Americas is supported currently
- **Forgetting to click "Finish Setup"** — profile is created but not associated, never activates

## Step 3: Verify Activation

Two ways to verify:

1. **Hub → Common Services → Tenant Management** → select tenant → **Deployment Profiles** tab → status should show **Complete**
2. **SCM → Insights → Prisma AIRS → Model Security** — dashboard should be visible with scan activity area

**Note:** Activation can take up to 2 hours per techdocs. Usually faster (minutes to 30 min). If still pending, the student can proceed with conceptual content.

## Step 4: Create Service Account for Scanning

**Techdocs:** https://docs.paloaltonetworks.com/ai-runtime-security/ai-model-security/model-security-to-secure-your-ai-models/get-started-with-ai-model-security/configure-identity-and-access-management

IAM for AIRS is managed through **Strata Cloud Manager → Common Services → Identity & Access**. AIRS has granular IAM options — highlight this to students as a selling point for enterprise customers.

**Prerequisites** (per techdocs):
- Active Deployment Profile (from Step 1)
- At least one TSG (from Step 2)

### Step 4a: Create Service Account

1. Navigate to **Strata Cloud Manager → Common Services → Identity & Access → Access Management**
2. Select the tenant (e.g., `syoungberg-api`)
3. Go to **Service Accounts** section
4. Create a new service account:
   - **Name:** Descriptive (e.g., `mlops-lab-scanner`)
   - **Assign Role:** **Superuser** (see Known Issue below)
5. **Download the credentials immediately** — contains CLIENT_ID and CLIENT_SECRET
   - **You cannot retrieve the secret later.** If lost, you must create a new SA.
6. Note the **TSG_ID** from the tenant details (Common Services → Tenant Management → select tenant → TSG ID shown at top)

The SA is automatically scoped to the TSG you're managing when you create it.

### Known Issue: Custom Roles Return 403 (as of March 2026)

**Bug:** Custom roles with Model Security permissions return HTTP 403 "Access denied" on all AIRS API endpoints, even when the correct permissions are enabled. Only the **Superuser** built-in role works reliably.

Per the techdocs, the correct setup for custom roles involves two steps:
1. **Role permissions:** Roles → Custom Roles → Enable AI Model Security → Save
2. **API permissions:** API → Add permissions → assign `ai_ms_pypi_auth`, `ai_ms.scans`, `ai_ms.security_groups`

Both steps are documented but custom roles still return 403 in practice. This may be a propagation issue or an enforcement bug post-GA. Until resolved, use **Superuser** for the lab SA.

**Teaching point for students:** This is a real-world gotcha. AIRS has granular IAM — in theory, you'd create different roles for different personas (CI/CD scanner, security admin, viewer). The granularity exists in the UI, but the enforcement has a bug. When talking to customers about AIRS RBAC:
- The *design* supports least-privilege — that's the right architecture
- The *implementation* is still maturing post-GA — flag this with your SE if a customer hits it
- Use Superuser for POCs/labs, plan for custom roles in production once the fix ships

### How PyPI Authentication Works

The AIRS Model Security SDK is distributed via a private PyPI repository hosted on Google Artifact Registry. To install it, the pipeline needs an authenticated PyPI URL:

1. **OAuth token**: SA credentials → `auth.apps.paloaltonetworks.com/oauth2/access_token` → bearer token
2. **PyPI URL**: Bearer token → `api.sase.paloaltonetworks.com/aims/mgmt/v1/pypi/authenticate` → time-limited PyPI URL with embedded credentials
3. **pip install**: `pip install --extra-index-url "$PYPI_URL" aimsdk` → installs from the private repo

The `scripts/get-pypi-url.sh` script handles steps 1-2. The workflow uses the URL in step 3. If the SA role doesn't have `ai_ms_pypi_auth` permission (or the bug above triggers), step 2 fails with 403.

### Least Privilege Note (Future State)

When the RBAC bug is fixed, the ideal configuration for the lab is:
- SDK authentication (`ai_ms_pypi_auth`) ✅
- Submit and read scans (`ai_ms.scans`) ✅
- Manage security groups (`ai_ms.security_groups`) ✅

In a production deployment, you'd separate further:
- CI/CD pipeline SA: scan-only (`ai_ms_pypi_auth` + `ai_ms.scans`)
- Security team: full admin (all permissions)
- Auditors: read-only

Hub IAM gives you the granularity to enforce separation of duties — once the enforcement matches the UI.

## Relationship: Deployment Profiles ↔ TSGs ↔ SCM

```
CSP Account (credit pool)
  └─ Deployment Profile (Model Security, 1500 credits)
       └─ Associated to TSG
            └─ SCM Instance (auto-provisioned if needed)
                 ├─ Model Security dashboard
                 ├─ Security Groups (auto-created defaults)
                 ├─ Service Accounts (you create)
                 └─ Scan history
```

- One TSG can have multiple deployment profiles (Model Security + Runtime + Red Team)
- Each deployment profile consumes credits independently
- SCM is provisioned once per TSG — subsequent profiles just add features

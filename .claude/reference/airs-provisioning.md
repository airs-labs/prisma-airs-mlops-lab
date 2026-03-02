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

## Step 4: Create Custom Role & Service Account for Scanning

IAM for AIRS is managed through **Hub → Common Services → Identity & Access**, NOT through SCM Settings. AIRS has granular IAM — highlight this to students as a selling point for enterprise customers.

### Step 4a: Create a Custom Role

1. Navigate to **Hub → Common Services → Identity & Access → Access Management**
2. Select the tenant (e.g., `syoungberg-api`)
3. Go to the **Roles** tab → **Custom Roles**
4. Click to create a new role
   - **Name:** e.g., `model-security-scanner`
   - **Description:** e.g., `Scanning role for MLOps pipeline`
5. Locate **AI Model Security** in the service list and enable it
6. For the lab, enable all Model Security permissions:
   - `ai_ms_pypi_auth` — required for SDK authentication
   - `ai_ms.scans` — required to submit and read scans
   - `ai_ms.security_groups` — required for managing security groups
7. Save the role

**Teaching point:** AIRS has really granular IAM options through Hub. In a real deployment, you'd create different roles for different personas — a CI/CD scanner role (scans only), a security admin role (security groups + policy), a viewer role (read-only dashboards). This maps to enterprise RBAC patterns.

### Step 4b: Create Service Account

The custom role must exist BEFORE creating the SA — you assign the role during SA creation.

1. Still in **Hub → Common Services → Identity & Access → Access Management**
2. Select the tenant → **Service Accounts** section
3. Create a new service account:
   - **Name:** Descriptive (e.g., `mlops-lab-scanner`)
   - **Assign Role:** Select the custom role created in Step 4a
4. **Download the credentials immediately** — contains CLIENT_ID and CLIENT_SECRET
   - **You cannot retrieve the secret later.** If lost, you must create a new SA.
5. Note the **TSG_ID** from the tenant details (Common Services → Tenant Management → select tenant → TSG ID shown at top)

The SA is automatically scoped to the TSG you're managing when you create it.

### Least Privilege Note

The scanning service account should have the permissions needed for the lab:
- SDK authentication (`ai_ms_pypi_auth`) ✅
- Submit and read scans (`ai_ms.scans`) ✅
- Manage security groups (`ai_ms.security_groups`) ✅

In a production deployment, you'd separate these further:
- CI/CD pipeline SA: scan-only (`ai_ms_pypi_auth` + `ai_ms.scans`)
- Security team: full admin (all permissions)
- Auditors: read-only

This is the principle students should carry to customer conversations: Hub IAM gives you the granularity to enforce separation of duties.

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

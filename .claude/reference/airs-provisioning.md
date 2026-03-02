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

After Model Security is activated in SCM:

1. Navigate to SCM → **Settings** → **Service Accounts**
2. Click **New Service Account** (or **Add**)
3. Configure:
   - **Name:** Descriptive (e.g., `mlops-lab-scanner`)
   - **Role:** Model Security (scanning permissions)
   - This gives scan-submit + result-read access. NOT admin access.
4. **Download the CSV** — contains CLIENT_ID and CLIENT_SECRET
   - **Do this immediately.** You cannot retrieve the secret later.
5. Note the **TSG_ID** from the tenant details (Common Services → Tenant Management → select tenant → TSG ID shown at top)

### Least Privilege Note

The scanning service account should have minimal permissions:
- Submit scans ✅
- Read scan results ✅
- Manage security groups ❌
- Manage users ❌
- Admin access ❌

This is the principle students should carry to customer conversations: CI/CD pipelines get scan-only credentials. Security teams manage policy in SCM with admin credentials. Separation of duties.

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

# Workshop Context

Background knowledge for the instructor-led Technical Services workshop. This file provides institutional context that flow files reference via `> CONTEXT:` markers.

## Prereq Lab: Runtime Security API (n8n)

Students completed the "Prisma AIRS - PS Lab - Runtime Security API - GCP & n8n" lab before this one. During that lab they:

1. **Created an AIRS Runtime Security API deployment profile** in the Customer Support Portal (CSP)
   - Profile type: Prisma AIRS → AI Runtime Security (API)
   - Named: `<username>-api`
2. **Created a new TSG** (Tenant Service Group) under a specific parent
   - CSP account: 1850598 - Palo Alto Networks - CoE
   - Parent TSG: "AIRS Workshop"
   - Sub-tenant name: `<username>-api`
3. **SCM was provisioned** on that TSG as part of the activation (~30 min)
4. **Built n8n workflows** that consume the AIRS Runtime Security API

Students SHOULD have a working TSG with SCM already provisioned when they start this lab.

## CSP & TSG Policy

- **Preferred:** Students use their own CSP account and TSG if they have one
- **Fallback:** The workshop CSP (account 1850598) is available with enough credits
- **Important:** This TSG will be used throughout the rest of the AIRS labs:
  - Model Security (this lab)
  - Red Team (separate lab)
  - Runtime Security (prereq lab, already done)
- Encourage students to think of this as their "AIRS home base" tenant

## Credit Consumption (Post-GA, late Feb 2026)

Model Security and Red Team went GA the last week of February 2026. Credit consumption changed significantly:

| Product | Credit Consumption | Notes |
|---------|-------------------|-------|
| **Model Security** | 1500 credits flat | Per deployment profile |
| **Red Team** | High (check CSP) | Per deployment profile |
| **Runtime Security (API)** | Varies by API call volume | Based on max API calls/day setting |
| **Runtime Security (Network/FW)** | Varies by vCPU | Based on firewall sizing |

**Why this matters for students:**
- They need to understand credit impact for customer conversations
- Stacking multiple AIRS products on one TSG = cumulative credit consumption
- The "Calculate Estimated Cost" button in CSP shows exact impact before committing
- Post-GA pricing is significantly higher than preview/beta pricing was

## Provisioning Timeline

| Scenario | Expected Time |
|----------|--------------|
| Associate to existing TSG with SCM already provisioned | Instant to minutes |
| Associate to existing TSG, SCM not yet provisioned | 15-30 minutes |
| Create brand new TSG + provision everything | 30-60 minutes |
| Techdocs worst case | Up to 2 hours |

**Strategy:** Kick off provisioning in Module 0, continue with Modules 1-3 while it completes. Verify before Module 4.

## Workshop Infrastructure

- **CSP Account:** 1850598 - Palo Alto Networks - CoE
- **Parent TSG:** AIRS Workshop
- **GCP Folder:** 187320463531 (from scenario config)
- **GCP Project Pattern:** `{email_prefix}-prod`
- **Region:** us-central1 (GCP), United States - Americas (CSP/SCM)

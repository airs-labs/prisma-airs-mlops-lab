# Activation & Deployment Profile Setup

## Topics to Cover (in order)

1. Deployment profiles — what they are, how they activate features on a Prisma AIRS tenant
2. CSP (Customer Support Portal) — where deployment profiles are created and managed
3. Tenant association — linking a deployment profile to an existing TSG (NOT creating a new one)
4. SCM activation — verifying AI Model Security appears in Strata Cloud Manager
5. Credential re-validation — ensuring Module 0 credentials work for Model Security scanning

## How to Explore

- Reference the AIRS tech docs: `.claude/reference/airs-tech-docs/ai-model-security.md` (section: "Create a Deployment Profile")
- Reference the activation docs: the PoV test scenarios prerequisite checklist
- Walk through CSP: https://support.paloaltonetworks.com → Products → Software/Cloud NGFW Credits
- Walk through Hub: https://apps.paloaltonetworks.com/apps → Tenant Management

## Student Activities

- Create a deployment profile in CSP: Prisma AIRS → Model Scanning (preview)
- Associate the deployment profile with their EXISTING tenant (critical: do NOT create a new one)
- Verify in SCM: navigate to AI Security → AI Model Security
- Re-validate credentials: run a test scan to confirm auth works
- Understand least-privilege: discuss what permissions a scanning SA should have

## Key Gotchas

- **Activation delay**: Deployment profile activation can take up to 2 hours. If pending, continue with conceptual work and come back.
- **Wrong tenant**: If a student accidentally creates a new tenant instead of using their existing one, they will lose SCM config. Identify the current tenant name/ID BEFORE starting.
- **Credentials scope**: Students may have admin credentials from Module 0. Discuss why a production pipeline should use a restricted SA with scan-only permissions.

## Customer Talking Point

"Adding Model Security to an existing AIRS deployment is a deployment profile and a tenant association — not a new infrastructure deployment. Your existing SCM, IAM, and service accounts carry over. The activation model is designed for incremental adoption."

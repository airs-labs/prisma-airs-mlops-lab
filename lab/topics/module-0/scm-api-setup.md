# SCM API Service Account Setup

**Track: @ts-workshop only**

## Topics to Cover (in order)

1. AIRS IAM model — how Tenant Service Groups (TSGs), service accounts, roles, and permissions work
2. TSG hierarchy — parent TSG (organization level) vs child TSG (AIRS-specific)
3. Least-privilege principle — why the scanning pipeline should only have scan submission and result reading permissions
4. SCM IAM API — creating service accounts and custom roles programmatically
5. OAuth2 client credentials flow — how CLIENT_ID + CLIENT_SECRET + TSG_ID authenticate scan requests

## How to Explore

- Use Context7 MCP to look up SCM IAM API documentation
- Read the AIRS tech docs in `.claude/reference/airs-tech-docs/ai-model-security.md` for model security API reference
- Use the parent TSG service account (from prework) to authenticate API calls
- The SCM API base URL and auth endpoints are documented in the AIRS reference material

## Student Activities

- Identify what API permissions a scanning-only service account needs
- Use Claude + Context7 to discover the SCM IAM API endpoints for:
  - Creating a custom role with specific permissions
  - Creating a service account
  - Assigning the custom role to the service account
- Create the service account in the AIRS child TSG
- Verify it can authenticate and submit a scan request
- Set the credentials as GitHub repository secrets

## What This Demonstrates

This exercise shows how Claude Code can work with unfamiliar APIs in real time — using documentation lookup (Context7), API exploration, and iterative problem-solving. The student sees the AI-assisted operations workflow: describe the goal → Claude finds the API → builds the request → executes and verifies.

## Customer Talking Point

"When customers ask about AIRS RBAC, we show them that service accounts can be scoped to exactly the permissions needed. A scanning pipeline doesn't need admin access — it needs scan submission and result reading. This is the same least-privilege pattern they already apply to their infrastructure."

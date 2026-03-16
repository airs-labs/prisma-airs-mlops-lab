# Scan Output Enrichment — Deep Dive

> Supplemental depth for /lab:explore. Essential concepts are taught in the Module 5 flow.

## Additional Topics

### Scan Response Anatomy
The SDK returns a structured response with: `eval_outcome` (ALLOWED/BLOCKED/PENDING/ERROR), `eval_summary` (aggregate counts: rules_passed, rules_failed, rules_total), `uuid` (unique scan identifier), `labels` (key-value pairs), `model_formats` (detected formats), `scanner_version`. This is the complete data available programmatically. Per-rule details (which specific rule failed, violation descriptions, remediation steps) are NOT available via the SDK — only through SCM.

**Explore:** Run a scan with `--output-json scan-result.json` and examine the full response. Compare it to what you see in SCM for the same scan UUID. What information is in SCM but NOT in the JSON?

### GitHub Actions Step Summaries
`$GITHUB_STEP_SUMMARY` is a special file in GitHub Actions — any markdown written to it renders on the workflow run page as a formatted summary. This is the best available mechanism for surfacing scan results to developers without requiring them to log into SCM. Write a rich summary: verdict badge, rule counts, scan UUID, labels, and a direct link to the SCM scan details page.

**Explore:** Read the GitHub Actions documentation for `$GITHUB_STEP_SUMMARY`. What markdown features are supported? Can you include tables, links, badges? Build a template that includes all useful scan information.

### The Product Gap Conversation
Per-rule evaluation details require SCM access. This creates a workflow friction: developer triggers pipeline → scan fails → developer sees "BLOCKED" with aggregate counts → developer files ticket with security team → security team logs into SCM → finds scan UUID → looks up per-rule details → relays information back. This round-trip takes hours. The honest framing for customers: "Here's what we can show in CI/CD today. For per-rule details, here's the one-click SCM link. We're actively working on bringing more detail into the SDK response."

**Explore:** Design a developer-friendly scan report that makes the best of available data. What would minimize the need for developers to open SCM? Can the scan UUID be hyperlinked directly to the SCM details page?

### Data API for Advanced Integration
For teams that need programmatic access to per-rule details, the data API at `/aims/data/v1/scans/{uuid}/evaluations` and `/aims/data/v1/scans/{uuid}/rule-violations` provides this information. This requires additional API calls after the initial scan and may need elevated permissions.

**Explore:** If you discovered the data API during Module 4's Discovery Challenge, try integrating it into the pipeline summary. What additional information becomes available?

## Key Files
- `airs/scan_model.py` — scanner CLI with `--output-json` flag
- `.github/workflows/gate-2-publish.yaml` — where the summary step goes
- `.claude/reference/model-security-scanning.md` — API surface details

## Student Activities
- Add `--output-json` to the scan step in Gate 2 workflow
- Write a post-scan step that reads the JSON and builds a markdown summary for `$GITHUB_STEP_SUMMARY`
- Include verdict, rule counts, scan UUID, labels, and SCM link
- Discuss: how would you frame the per-rule detail limitation to a customer? What's the honest answer AND the forward-looking message?

## Customer Talking Point
"Developers want actionable feedback in their existing tools. Today the SDK gives aggregate pass/fail counts and a scan UUID that links to full details in SCM. For teams that need per-rule details without leaving their CI tool, that is a product enhancement conversation we can have."

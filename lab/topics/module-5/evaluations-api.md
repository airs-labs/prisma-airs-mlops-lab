# Scan Output Enrichment

## Topics to Cover (in order)
1. What the scan response contains -- eval_outcome, eval_summary (rules_passed/failed/total), uuid, labels
2. What is NOT available -- per-rule evaluation details require SCM access, no public API endpoint for rule-level data
3. Bridging the gap -- using scan UUID as a link to SCM, surfacing aggregate data in CI/CD
4. GitHub Actions job summaries -- rendering scan results as markdown tables in workflow run UI
5. The product gap conversation -- how to discuss API limitations honestly with customers

## How to Explore
- Run a scan with `--output-json` and examine the full response structure
- Use `get_scan(uuid)` from the SDK to see what fields are available after a scan completes
- Look at `$GITHUB_STEP_SUMMARY` in the GitHub Actions docs for formatting options

## Student Activities
- Add `--output-json` to the scan step in Gate 2 workflow
- Write a post-scan step that reads the JSON and builds a markdown summary for `$GITHUB_STEP_SUMMARY`
- Include verdict, rule counts, scan UUID, labels, and a note about where to find per-rule details
- Discuss with Claude: what would you tell a customer who wants per-rule details in their CI/CD pipeline?

## Customer Talking Point
"Developers want actionable feedback in their existing tools. Today the SDK gives aggregate pass/fail counts and a scan UUID that links to full details in SCM. For teams that need per-rule details without leaving their CI tool, that is a product enhancement conversation we can have."

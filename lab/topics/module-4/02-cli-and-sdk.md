# AIRS CLI and SDK

## Topics to Cover (in order)
1. SDK installation -- authenticated PyPI, `model-security-client` package
2. CLI basics -- `model-security scan`, exit codes, basic options
3. SDK usage -- `ModelSecurityAPIClient`, `scan()`, `get_scan()`, `list_scans()`
4. Response fields -- uuid, eval_outcome (ALLOWED/BLOCKED/PENDING/ERROR), eval_summary
5. Exit code handling -- how pipelines use exit codes for go/no-go decisions

## Key Files
- `airs/scan_model.py` -- project's scanning wrapper
- `scripts/test_airs_sdk.py` -- test harness exercising all SDK operations
- `docs/airs-tech-docs/ai-model-security.md` -- full reference documentation

## How to Explore
- Read scan_model.py: how does it detect source type? How does it resolve security groups?
- Run test_airs_sdk.py to see the SDK in action
- Scan a known-safe model from GCS: `gs://your-model-bucket/approved-models/cloud-security-advisor/v2.0.0`

## Student Activities
- Scan a known-safe model -- what does ALLOWED look like in the response?
- Scan a pickle model -- compare the response to the safe model
- Use `get_scan(uuid)` to retrieve a past scan result -- what fields are available?

## Key Insight
eval_outcome has exactly 4 values: ALLOWED, BLOCKED, PENDING, ERROR. Values like MALICIOUS or FAIL do not exist in the SDK. BLOCKED means a blocking-enabled rule in the security group detected an issue.

# Security Groups

## Topics to Cover (in order)
1. What security groups are -- policy containers with rules and source type bindings
2. Source types -- LOCAL, GCS, HUGGING_FACE, S3, AZURE_BLOB
3. Default security groups -- one per source type, auto-selected when no UUID specified
4. UUID matching -- security group UUID must match the source type of the model being scanned
5. Custom groups -- creating warning-only vs blocking groups for different pipeline stages

## How to Explore
- Look at the security groups table in `airs/scan_model.py` (SECURITY_GROUPS dict)
- SCM console: navigate to AI Model Security -> Security Groups
- This project has 5 groups: local, gcs-default, hf, warn (GCS), block (GCS)
- Reference: docs/airs-tech-docs/ai-model-security.md for full documentation

## Student Activities
- Create a new "blocking" security group for GCS with all rules set to block
- Create a "warning-only" security group for GCS with all rules set to warn
- Scan the same model against both groups -- compare ALLOWED vs BLOCKED outcomes
- What happens if you try to scan a GCS model with a LOCAL security group?

## Key Insight
The same model, scanned with the same rules, can produce ALLOWED (warning group) or BLOCKED (blocking group). The difference is whether the rule has Blocking=On in SCM. `rules_failed` counts ALL rule detections; `eval_outcome=BLOCKED` only when a blocking rule fires.

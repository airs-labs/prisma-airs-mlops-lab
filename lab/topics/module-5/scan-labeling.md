# Scan Labeling

## Topics to Cover (in order)
1. What labels are -- key-value metadata attached to scan requests
2. Useful label keys -- gate, run_id, model_version, environment, base_model
3. How labels appear in SCM -- filtering and reporting by label
4. Pipeline integration -- adding labels to automated scan steps
5. Provenance tracking via labels -- connecting scans to specific pipeline runs

## How to Explore
- Check the AIRS SDK docs and release notes for label support
- Reference: docs/airs-tech-docs/ai-runtime-security-release-notes.md for latest features
- Look at how scan_model.py could be extended with a --labels argument

## Student Activities
- Add labels to a scan: `gate=gate2`, `run_id=$GITHUB_RUN_ID`, `model_version=v2.0.0`
- Submit labeled scans and verify labels appear in SCM reports
- Add standard labels to the Gate 2 scan step in the workflow
- Discuss: what labels would help an enterprise track models across environments?

## Customer Talking Point
"Labels connect scans to business context. When a CISO asks 'which models passed scanning this quarter?', labels make that query possible without digging through pipeline logs."

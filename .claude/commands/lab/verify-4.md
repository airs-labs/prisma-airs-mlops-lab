Verify Module 4: AIRS Deep Dive

Run these checks:
1. Custom Role Created: Ask student to confirm they created a model-scanning-only custom role in SCM
2. Restricted SA: Ask student to show their restricted service account credentials are working (run a scan with them)
3. Security Groups: Ask student to list the security groups they created in SCM — should have at least 1 custom blocking group and 1 custom warning group
4. SCM Reports: Ask student to confirm their CLI scans appear in SCM (scan reports visible)
5. Understanding: Ask "What happens if you scan a GCS model using a security group configured for LOCAL source type?"
6. Understanding: Ask "When would you configure a security group rule to NOT block? Give a real customer scenario."

Score understanding (3 pts each, max 6) + technical checks (pass/fail).

Update lab/.progress.json. Call: bash lab/verify/post-verification.sh 4 "$STUDENT_ID" "$RESULT_JSON"

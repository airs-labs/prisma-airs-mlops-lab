Verify Module 5: Integrate AIRS into Pipeline

Run these checks:
1. Gate 2 Scan: Check if the student modified gate-2-publish.yaml to include an AIRS scan step — read .github/workflows/gate-2-publish.yaml and verify a scan step exists between merge and publish
2. Gate 3 Manifest: Check if gate-3-deploy.yaml has manifest verification — read the workflow file
3. Pipeline Run: Ask student to show a successful Gate 2 run with AIRS scan results in the GH Actions summary
4. Labels: Check if scans have labels (gate, run_id, model_version) — ask student to show SCM scan with labels
5. Evaluations: Check if pipeline outputs evaluation details in GH Actions summary
6. Understanding: Ask "Walk me through what happens when a model fails the AIRS scan in Gate 2. What stops? What doesn't?"

Score understanding (3 pts, max 3) + technical checks (pass/fail).

Update lab/.progress.json. Call: bash lab/verify/post-verification.sh 5 "$STUDENT_ID" "$RESULT_JSON"

Verify Module 0: Environment & Claude Code Setup

Run these checks:
1. GCP Auth: Run `gcloud auth list` — verify an active account
2. GH CLI: Run `gh auth status` — verify authenticated
3. AIRS Credentials: Check if MODEL_SECURITY_CLIENT_ID and MODEL_SECURITY_CLIENT_SECRET are set as GitHub secrets (run `gh secret list`)
4. Repo Structure: Verify lab/ directory exists with topic files
5. Claude Comprehension: Ask the student: "In your own words, describe the 3-gate pipeline architecture of this project."

Evaluation:
- All 4 technical checks must pass
- Student's description should mention: Gate 1 (train), Gate 2 (merge+publish), Gate 3 (deploy), and that AIRS scanning is not yet integrated

Record results in lab/.progress.json under modules.0:
- status: "complete" or "incomplete"
- verified: true/false
- checks_passed: [list of passed check names]

If all checks pass AND the student demonstrates understanding:
- Mark module 0 as complete and verified
- Congratulate them and suggest starting Module 1 with /lab:module 1

Call the verification POST script if it exists: bash lab/verify/post-verification.sh 0 "$STUDENT_ID" "$RESULT_JSON"

Verify Module 6: The Threat Zoo

Run these checks:
1. Threat Models: Ask student to list the threat models they created (should be at least 2)
2. Scan Results: Ask student to show BLOCKED scan results for malicious models
3. Format Comparison: Ask student to show side-by-side scan results (pickle vs safetensors)
4. Understanding: Ask "Explain how Python's __reduce__ method enables code execution in pickle files. Why does torch.load() trigger this?"
5. Understanding: Ask "What is the 'Stored In Approved File Format' AIRS rule checking for?"

Score understanding (3 pts each, max 6) + technical checks (pass/fail).

Update lab/.progress.json. Call: bash lab/verify/post-verification.sh 6 "$STUDENT_ID" "$RESULT_JSON"

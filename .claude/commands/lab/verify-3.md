Verify Module 3: Deploy & Serve

Run these checks:
1. App Deployed: Run `gcloud run services describe cloud-security-advisor --region=us-central1 --format='value(status.url)'` — should return a URL
2. App Responds: Curl the URL's /health endpoint or send a test chat message
3. Architecture Understanding: Ask "Why is the model NOT in the Cloud Run container? Draw the architecture (describe it verbally)."
4. Inference Understanding: Ask "What is rawPredict and why does the app use model='openapi' instead of the actual model name?"

Score understanding questions (3 pts each, max 6). Technical checks are pass/fail.

IMPORTANT: This is the end of Act 1 (Build It). Before suggesting Module 4, note:
"Module 4 is the start of the security deep dive. There is typically an instructor-led presentation on AIRS value proposition and customer scenarios between Modules 3 and 4. Check with your instructor."

Also ask the student to generate a summary of what they've built so far — architecture, model choice, training decisions, deployment — formatted for group discussion.

Update lab/.progress.json. Call: bash lab/verify/post-verification.sh 3 "$STUDENT_ID" "$RESULT_JSON"

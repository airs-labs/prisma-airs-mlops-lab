Verify Module 2: Train Your Model

Run these checks:
1. Training Output: Check if a training adapter exists in GCS — run `gcloud storage ls gs://your-model-bucket/raw-models/` and look for the student's model
2. Understanding Check: Ask "What is the difference between a LoRA adapter and a fully merged model? Why do we merge before deployment?"
3. Merge Understanding: Ask "What does merge_adapter.py do with the extra_special_tokens field and why?"

Technical checks + understanding questions. Score the understanding questions (3 pts each, max 6).

Update lab/.progress.json under modules.2. Add points to leaderboard_points.

Call: bash lab/verify/post-verification.sh 2 "$STUDENT_ID" "$RESULT_JSON"

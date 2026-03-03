# Module 3 Flow: Deploy & Serve

> INTERNAL PLAYBOOK — never shown to students.
> Engagement points tracked during module. All other scoring happens during /lab:verify-3.

## Points Available

| Source | Points | When |
|--------|--------|------|
| Engage: Architecture understanding (3.1) | 1 | During flow |
| Engage: Security gap awareness (3.4) | 1 | During flow |
| Technical: App deployed | 2 | During verify |
| Technical: App responds | 2 | During verify |
| Quiz Q1: Why custom model / self-host | 3 | During verify |
| Quiz Q2: Serving components | 3 | During verify |
| Quiz Q3: Pipeline + security gap | 3 | During verify |
| **Total** | **15** | |

---

## Challenge 3.1: Architecture First

### Learning Objectives

The student should be able to:
- Explain what the app is and why it uses a self-hosted fine-tuned model
- Describe the decoupled serving architecture and why model and app are separated
- Understand at a high level how the app calls the model, what vLLM does, and what chat templates are

### Key Concepts

Explore these through the project files. Show code first, then discuss. One concept at a time.

1. **What You Built and Why**
   - This is a Cloud Security Advisor — an internal cybersecurity chatbot fine-tuned on NIST frameworks. The reason it's self-hosted (not just calling ChatGPT) is control: data sovereignty, compliance, specialization, no vendor lock-in.
   - Connect to Module 2: remind them what dataset they trained on and why.
   - Check: Why would a customer self-host instead of using a commercial API?

2. **The Container — What's NOT There**
   - Show: Read `Dockerfile` and display it inline. Let the student look at it.
   - Explore: What's missing? No model weights, no PyTorch, no CUDA, no GPU drivers. It's `python:3.12-slim` running `uvicorn`. That's it. So if this container can't run a model... where does the actual inference happen?
   - This naturally leads to the decoupled architecture: app on Cloud Run (cheap CPU, 512MB RAM) vs model on Vertex AI endpoint (expensive GPU running vLLM).
   - Check: Why would you want this separation? (cost, scaling, independent updates, security scan insertion points)

3. **The App Layer — How Thin It Is**
   - Show: Read `src/airs_mlops_lab/serving/server.py` and display the chat endpoint. It's ~5 lines: receive message, call inference client, return reply. Zero ML logic.
   - Show: Read `src/airs_mlops_lab/serving/inference_client.py` and display the `chat()` method. Walk through what's happening at a high level:
     - It builds a prompt using chat template tokens (`<|im_start|>`, `<|im_end|>`) — this is how the model understands conversation turns. Different models use different formats.
     - It calls a Vertex AI `rawPredict` endpoint with a GCP auth token.
     - It uses `model: "openapi"` — a Vertex AI quirk where the served model name gets overridden.
   - Don't go deep on any of these — just enough that the student knows what's happening. The point is: the app is a thin client that formats requests and passes them through.
   - Check: Can the student trace the request flow? Browser → app → Vertex AI → vLLM on GPU → response back.

4. **The Visual**
   - Show: [VISUAL] Generate a request flow diagram showing the full architecture: Browser → Cloud Run (CPU, no model) → auth boundary (GCP token) → Vertex AI → vLLM (GPU, model weights). Include a callout about the security gap. Output to `lab/.visuals/m3-c1-request-flow.html`.
   - Have the student trace the full flow in their own words. Where does auth happen? Where does the heavy compute happen?

> **ENGAGE**: Now the security question. The auth controls who can CALL the model. But what controls whether the model ITSELF is safe? A poisoned model would serve through this exact same auth flow. Where in this architecture would you insert a security check?
> Award 1 pt for meaningful engagement. Effort-based, not correctness.

### Action

No commands to run. This is a comprehension challenge — learning happens through code exploration and discussion.

### Debrief

- This architecture is the standard pattern for enterprise ML deployments — same pattern behind OpenAI, Anthropic, and self-hosted setups. The layers differ but the structure is the same.
- The customer question: "What scans happened between training and deployment?" For most organizations, the answer is none.
- Foreshadow: nothing stops a compromised model from loading onto that GPU. That changes in Module 5.

### Deep Dive

For `/lab:explore`: `lab/topics/module-3/serving-architecture.md`
Covers additional depth on: vLLM internals, chat template syntax, rawPredict details, Vertex AI-specific constraints.

---

## Challenge 3.2: Run the Pipeline

### Learning Objectives

The student should be able to:
- Describe what Gate 2 (merge + publish) and Gate 3 (deploy) do
- Trigger pipeline workflows and monitor their progress
- Understand that the current pipeline has NO security checks (to be added in Module 5)

### Key Concepts

Teach these BEFORE triggering the workflows. One at a time, wait for response.

1. **Gate 2: Merge and Publish**
   - Core idea: Gate 2 takes the raw training output (LoRA adapter + base model reference) and produces a single merged model in safetensors format. The merge is simple matrix addition (CPU, no GPU needed). The merged model is published to GCS with a manifest tracking provenance.
   - Show: Read `.github/workflows/gate-2-publish.yaml` and display the key steps — merge_adapter, publish to GCS, manifest update. Point out what is NOT there: no AIRS scan, no provenance verification. This is intentional on `lab-start` — the student adds security in Module 5.
   - Check: Does the student understand what goes IN (adapter + base) and what comes OUT (merged safetensors + manifest)? Why is merge done on CPU?

2. **Gate 3: Deploy**
   - Core idea: Gate 3 takes the published model from GCS and deploys it two ways: (1) a Vertex AI endpoint with a vLLM container on GPU for inference, and (2) a Cloud Run service for the application. GPU provisioning takes 15-30 minutes.
   - Show: Read `.github/workflows/gate-3-deploy.yaml` and display the key steps — verify manifest, deploy endpoint, deploy app. Again, note the security gaps: manifest verification exists in the workflow but is not enforcing yet.
   - Check: Can the student explain the two deployment targets (GPU endpoint + CPU app) and why they're separate? What does the 15-30 min wait come from?

**Naming convention:** There's an important distinction between the `output_name` the student chose in Gate 1 (their training experiment name) and the `model_name` used in Gate 2. Gate 2's `model_name` is the **application model identity** — it must be `cloud-security-advisor` because that's the name Gate 3 and the deployment infrastructure expect. Guide the student through this distinction.

### Action

Now that the student understands what will happen, execute the pipeline.

1. **Trigger Gate 2** — Merge and publish the trained model:
   ```bash
   # model_name MUST be "cloud-security-advisor" — Gate 3 deploys this application name
   BRANCH=$(git branch --show-current)
   gh workflow run "Gate 2: Publish Model" -r "$BRANCH" \
     -f model_source="gs://<bucket>/raw-models/<model-name>/<run-id>" \
     -f base_model="Qwen/Qwen2.5-3B-Instruct" \
     -f model_name="cloud-security-advisor"
   ```
   Use the adapter path from the student's Gate 1 training output (stored in progress.json or from `gs://` listing).

2. **Monitor Gate 2:**
   ```bash
   gh run list --limit 5
   gh run watch
   ```

3. **Trigger Gate 3** — Deploy the merged model:
   ```bash
   gh workflow run "Gate 3: Deploy" -r "$BRANCH" \
     -f model_version="v1.0.0" \
     -f target_env="staging"
   ```

4. **Monitor Gate 3** — This takes 15-30 minutes (GPU provisioning). Use this wait time to discuss the deployment architecture or let the student explore topics.

### Debrief

- The pipeline is now running. While waiting for Gate 3, revisit the artifact flow: where does the model physically live at each stage?
- Note: On `lab-start`, there are NO AIRS scans in Gate 2 and NO manifest enforcement in Gate 3. The student will add these in Module 5.
- The customer insight: most organizations have this exact blind spot — models flow from training to production with zero security checks.

### Deep Dive

For `/lab:explore`: `lab/topics/module-3/deployment-pipeline.md`
Covers additional depth on: pipeline chaining (auto_chain), app-only deploys, manifest provenance system.

---

## Challenge 3.3: Test Your App

### Learning Objectives

The student should be able to:
- Access and interact with their deployed application
- Observe fine-tuning effects and relate response quality to training parameters
- Identify how the thin client architecture works in practice

### Key Concepts

1. **Cloud Run Authentication (Let them discover this)**
   - Core idea: Cloud Run services can be deployed as **authenticated** (require IAM credentials) or **public** (allow unauthenticated access). This deployment requires authentication — a security best practice for internal services. In enterprise environments, exposing ML inference endpoints publicly is a risk.
   - Show: Get the Cloud Run URL and give it to the student:
     ```bash
     gcloud run services describe cloud-security-advisor --region=us-central1 --format='value(status.url)'
     ```
     Tell them to open it in a browser. **Expect a 403 Forbidden.** Do NOT pre-emptively warn them or set up the proxy — let them hit the wall and report back.
   - When they report the 403: Explain that the 403 means Cloud Run is doing its job — rejecting unauthenticated requests. This is the same pattern used in production: internal services are not publicly accessible. Then introduce `gcloud run services proxy`:
     ```bash
     gcloud run services proxy cloud-security-advisor --region=us-central1 --port=8080
     ```
     This creates an authenticated tunnel. If the `cloud-run-proxy` component isn't installed, gcloud will prompt — say yes. To keep it running in the background:
     ```bash
     nohup gcloud run services proxy cloud-security-advisor --region=us-central1 --port=8080 > /dev/null 2>&1 &
     ```
     The student accesses the app at **http://localhost:8080**.
   - Check: Does the student understand why the direct URL returned 403? What is the proxy doing under the hood? (Forwarding requests with GCP auth credentials attached.)

2. **Fine-Tuning Quality and Training Steps**
   - Core idea: With 50 training steps, the model will show some cybersecurity domain influence but may still be generic in many areas. With 200+ steps, specialization becomes more pronounced. This is the fundamental tradeoff between training cost and model quality. The student should observe this firsthand.
   - Show: With the proxy running, have the student interact with the chat interface at `http://localhost:8080`.
   - Check: Can the student tell the difference between their fine-tuned model and a generic chatbot? What cybersecurity knowledge is present? What is missing?

### Action

1. Give the student the Cloud Run URL — let them try it directly (expect 403)
2. When they report the 403, teach Cloud Run authentication and set up the proxy
3. With proxy running, test with domain-specific questions:
   - "What are the key components of the NIST Cybersecurity Framework?"
   - "How should an organization respond to a ransomware attack?"
   - "Explain zero trust architecture in simple terms."
4. Test with out-of-domain questions to see where fine-tuning boundaries are
5. If the app returns errors after getting past auth, troubleshoot:
   - Check Vertex AI endpoint status in console
   - Verify Cloud Run SA has `roles/aiplatform.user`
   - Check logs: `gcloud run services logs read cloud-security-advisor --region=us-central1`

### Debrief

- Discuss what the student observed about model quality. Connect training steps to response quality.
- Revisit the auth lesson: the 403 was a feature, not a bug. Enterprise ML services are authenticated by default.
- The model is live behind authentication. But authentication controls who can *use* the model — it says nothing about whether the model itself is safe. Right now there are no security controls on what model is serving.

### Deep Dive

None — this challenge is experiential. The learning happens through interaction.

---

## Challenge 3.4: Explain the Architecture (Synthesis)

### Learning Objectives

The student should be able to:
- Articulate the full architecture end-to-end: where the model lives, where the app lives, how they communicate
- Trace artifact flow through all three gates
- Identify the critical security gap: no scans between training and deployment

### Key Concepts

1. **Full Pipeline Architecture**
   - Core idea: The student has now built and used every component. This challenge asks them to synthesize it all into a coherent mental model. No new concepts — this is about connecting everything.
   - Show: [VISUAL] Generate a full pipeline architecture diagram showing all three gates, artifact flow, and the serving architecture. Output to `lab/.visuals/m3-c4-full-pipeline.html`. Include: Gate 1 (train) → Gate 2 (merge + publish) → Gate 3 (deploy endpoint + deploy app) → Live application.
   - Check: Have the student walk through the entire pipeline verbally. At each stage: what goes in, what comes out, where does the artifact live, and what checks happen (answer: none yet).

> **ENGAGE**: "What security scans happened between training and deployment?"
> This is a trick question. The answer is none — and that's the entire point of the next act.
> Award 1 pt for meaningful engagement. The key insight: they just deployed a model pulled from the public internet, trained on a public dataset, with zero security checks.

### Action

No commands. The student demonstrates synthesis through conversation.

### Debrief

- This is the capstone of Act 1 ("Build It"). The student has built a complete ML pipeline: train, merge, publish, deploy.
- The transition into Act 2: "If someone published a malicious model on HuggingFace and your pipeline downloaded it, what would stop it from executing arbitrary code in your training infrastructure or on your GPU endpoint?" The answer, right now, is nothing.
- Ask the student to prepare a brief summary of what they built for the group discussion: architecture, model choice, training decisions, and the security gap.

### Deep Dive

None — synthesis challenge. All relevant topics are covered in Challenges 3.1 and 3.2.

---

## End of Act 1

This is the end of Act 1 ("Build It"). The student has built a complete ML pipeline: train, merge, publish, deploy.

If hard stops are enabled (check `lab.config.yaml` scenario config for `hard_stops: true`):
Display: "HARD STOP — Module 3 Complete. There is typically an instructor-led AIRS presentation between Acts 1 and 2. Check with your instructor before starting Module 4."

Ask the student for any feedback on the module before wrapping up. Encourage them to submit via the feedback endpoint during verification.

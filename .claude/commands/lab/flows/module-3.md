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
- Explain what the app is, what problem it solves, and why it uses a custom fine-tuned model
- Describe the components of model serving: what vLLM does, what inference endpoints are, how the app talks to the model
- Understand chat templates at a high level — what they are and where they're handled in the stack

### Key Concepts

Teach these BEFORE the student takes action. One at a time, wait for response.

1. **What You Built and Why**
   - Core idea: This is a **Cloud Security Advisor** — an internal chatbot for SOC teams, fine-tuned on NIST Cybersecurity Framework, incident response procedures, and compliance guidance. The reason it's a custom model (not just calling ChatGPT) is control: the organization owns the model, controls the training data, can run it on-premise or in their own cloud, and doesn't send sensitive queries to a third-party API. This is the exact scenario customers bring to PANW — "we want to deploy our own model."
   - Show: Read `lab/LAB-3.md` overview and the dataset references from Module 2. Remind the student what they trained on (NIST cybersecurity Q&A dataset) and connect it to the use case.
   - Check: Can the student articulate why an organization would fine-tune and self-host instead of using a commercial API? (data sovereignty, compliance, specialization, cost at scale, no vendor lock-in)

2. **Model Serving: The Components**
   - Core idea: Model serving is how a trained model becomes something users can actually talk to. There are three layers:
     - **Serving framework (vLLM)** — Think of this like nginx but for ML models. It loads model weights onto a GPU, manages memory efficiently, handles concurrent requests, and exposes an API. vLLM specifically is popular because it's fast (PagedAttention for memory) and exposes an OpenAI-compatible API.
     - **Inference endpoint** — The API that accepts prompts and returns completions. The standard is OpenAI's format: `/v1/completions` (raw text in, text out) and `/v1/chat/completions` (structured messages in, message out). Most serving frameworks speak this format now.
     - **Application layer** — The user-facing app (our FastAPI service on Cloud Run). It handles auth, UI, business logic, and calls the inference endpoint. It does NOT run the model — it's just a client.
   - Show: [VISUAL] Generate a 3-layer architecture diagram showing: Application (Cloud Run, CPU) → Inference Endpoint (Vertex AI) → Serving Framework (vLLM on GPU with model weights loaded). Output to `lab/.visuals/m3-c1-serving-layers.html`.
   - Check: Can the student describe the role of each layer? What lives on GPU vs CPU? Why is the serving framework a separate component from the application?

3. **Chat Templates — Where Intelligence Meets Format**
   - Core idea: LLMs don't inherently understand "conversations." They predict the next token in a sequence. Chat templates are the formatting convention that turns a multi-turn conversation into a single text string the model can process. Different models use different templates — Qwen2 uses `<|im_start|>` markers, Llama uses `[INST]`, etc. Normally, the `/v1/chat/completions` endpoint handles this formatting automatically. When it's not available (as in our Vertex AI setup), the application has to construct the template manually.
   - Show: Read `src/airs_mlops_lab/serving/inference_client.py` and display the chat template construction section. Show how the conversation messages get formatted into a single prompt string with role markers. Keep it high level — the point is "this is what's happening under the hood" not "memorize this syntax."
   - Check: Does the student understand that chat isn't magic — it's formatted text? Where in the stack is this normally handled vs where we handle it? Why does the template format matter? (wrong format = garbage output even if the model is fine)

> **ENGAGE**: After covering the three layers, ask the student to think about this from a security perspective. If you were assessing this deployment, where are the trust boundaries? Where could an attacker insert themselves? The key insight: the model artifact itself is a trust boundary that nobody is checking right now.
> Award 1 pt for meaningful engagement. Effort-based, not correctness.

### Action

No commands to run for this challenge. This is a comprehension challenge.
The learning objectives are met through the Key Concepts checks above.

### Debrief

- This architecture (app → inference endpoint → serving framework) is the standard pattern for enterprise model deployments. It's how OpenAI, Anthropic, and enterprise self-hosted deployments all work — the layers may differ but the pattern is the same.
- The customer question that matters: "What scans happened between training and deployment?" In most organizations, the answer is none.
- Foreshadow: Right now, nothing stops a compromised model from being loaded onto that GPU. That changes in Module 5.

### Deep Dive

For `/lab:explore`: `lab/topics/module-3/serving-architecture.md`
Covers additional depth on: rawPredict internals, vLLM memory management, chat template syntax details, Vertex AI-specific constraints.

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

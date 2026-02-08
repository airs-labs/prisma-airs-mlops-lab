# Module 3: Deploy & Serve

## Overview

A trained model sitting in cloud storage does not help anyone. In this module, you will take your fine-tuned model from training artifacts to a live, running application. You will merge the LoRA adapter, publish the model, deploy it to a Vertex AI GPU endpoint, and deploy a thin application on Cloud Run that talks to it. By the end, you will have a working cybersecurity advisor chatbot you can interact with in a browser.

## Objectives

- Understand the decoupled inference architecture before deploying
- Run Gate 2 (merge + publish) and Gate 3 (deploy endpoint + deploy app)
- Test the live application and observe fine-tuning effects in responses
- Articulate the full architecture: where the model lives, where the app lives, how they communicate

## Prerequisites

- Module 2 complete (training finished, adapter in GCS)
- GCP authentication working, GitHub CLI authenticated
- Training output path known (from Module 2 verification)

## Time Estimate

~1 to 1.5 hours (includes ~15-30 minutes of deployment wait time for GPU provisioning)

---

## Challenges

### Challenge 3.1: Architecture First

You would not push a button labeled "Deploy to Production" without understanding what happens. Before you trigger anything, build a complete mental model of the inference architecture.

Use `/explore serving-architecture` in Claude Code for guided exploration.

Answer these questions:
- Why is the model NOT in the Cloud Run container? Where does it live?
- What is vLLM and why does this project use it for serving?
- What is `rawPredict`? How does Vertex AI route requests to the vLLM container?
- Why does the request payload use `model: "openapi"` instead of the actual model name?
- What is the Qwen2 chat template? Why does the app format messages with `<|im_start|>` tokens?
- Why does the app use `/v1/completions` instead of `/v1/chat/completions`?

Draw (or describe to Claude) the full request flow: User browser --> Cloud Run app --> Vertex AI rawPredict --> vLLM container --> GPU inference --> response back.

<details><summary>Hint 1: Concept</summary>

This is a *decoupled* architecture. The model runs on GPU infrastructure (Vertex AI endpoint with vLLM), and the application runs on lightweight infrastructure (Cloud Run with 512MB RAM). They communicate over an authenticated HTTP API. This separation means you can scale, update, and secure each component independently.

</details>

<details><summary>Hint 2: Approach</summary>

Read three files to understand the architecture:
1. `src/airs_mlops_lab/serving/inference_client.py` -- the client that calls Vertex AI
2. `src/airs_mlops_lab/serving/server.py` -- the FastAPI application
3. `Dockerfile` -- what is (and is not) in the container

Trace a request from the user to the model and back.

</details>

<details><summary>Hint 3: Implementation</summary>

Ask Claude:

```
"Read inference_client.py and trace a chat request from the chat() method all the way to the Vertex AI endpoint. Explain the rawPredict call, the chat template formatting, and why we use model='openapi'."
```

Key architectural details:
- The app container has NO model weights, NO PyTorch, NO GPU -- just FastAPI + httpx + google-auth
- Auth uses `google.auth.default()` for access tokens (not identity tokens)
- Vertex AI's vLLM launcher overrides the served model name to "openapi" -- you must match this in requests
- The Vertex AI vLLM build only exposes `/v1/completions`, not `/v1/chat/completions` -- so the app constructs the chat template manually in the prompt

</details>

---

### Challenge 3.2: Run the Pipeline

Time to deploy. You will trigger Gate 2 (merge + publish) followed by Gate 3 (deploy endpoint + deploy app).

**Important context:** On the `lab-start` branch, there are NO AIRS scans in Gate 2 and NO manifest verification in Gate 3. The pipeline currently runs without any security checks. You will add those in Module 5.

Use `/explore deployment-pipeline` in Claude Code for guided exploration.

**Step 1: Trigger Gate 2** -- This merges your LoRA adapter with the base model and publishes the merged model to GCS.

**Step 2: Trigger Gate 3** -- This deploys the merged model to a Vertex AI endpoint (GPU) and deploys the application to Cloud Run.

<details><summary>Hint 1: Concept</summary>

Gate 2 takes the raw training output (adapter + base model) and produces a single merged model in safetensors format. Gate 3 takes the merged model, deploys it on a Vertex AI endpoint with a vLLM serving container, and deploys the Cloud Run application that talks to it. Deployment involves GPU provisioning, which takes 15-30 minutes.

</details>

<details><summary>Hint 2: Approach</summary>

Use `gh workflow run` to trigger each gate. You will need to provide the correct input parameters -- particularly the `model_source` path from your Gate 1 training output. Check the workflow files or ask Claude what inputs each gate expects.

</details>

<details><summary>Hint 3: Implementation</summary>

Trigger Gate 2 (merge + publish):
```bash
# Use the adapter path from your Gate 1 output
gh workflow run "Gate 2: Publish Model" \
  -f model_source="gs://your-model-bucket/raw-models/my-security-advisor/<run-id>" \
  -f base_model="Qwen/Qwen2.5-3B-Instruct" \
  -f model_name="my-security-advisor"
```

Wait for Gate 2 to complete, then trigger Gate 3 (deploy):
```bash
gh workflow run "Gate 3: Deploy" \
  -f model_version="v1.0.0" \
  -f target_env="staging"
```

Monitor both:
```bash
gh run list --limit 5
gh run watch
```

Gate 3 deployment takes 15-30 minutes (GPU provisioning + model loading). Be patient.

</details>

---

### Challenge 3.3: Test Your App

Once deployment is complete, your cybersecurity advisor is live. Time to talk to it.

Find your Cloud Run URL from the Gate 3 deployment output (or from the GCP console). Open it in a browser and start a conversation.

Test it with questions like:
- "What are the key components of the NIST Cybersecurity Framework?"
- "How should an organization respond to a ransomware attack?"
- "Explain zero trust architecture in simple terms."
- "What is the difference between authentication and authorization?"

Observe:
- Does the model respond with cybersecurity domain knowledge?
- Can you tell the difference between the fine-tuned model and a generic chatbot?
- How fast are the responses? (This relates to vLLM batching and GPU performance)
- Are there any obvious quality issues? (Short training runs produce lower quality)

<details><summary>Hint 1: Concept</summary>

The quality of responses depends on how many training steps you ran. With 50 steps, you will see some NIST influence but the model may still be generic in many areas. With 200+ steps, the cybersecurity specialization becomes more pronounced. This is the tradeoff between training cost and model quality.

</details>

<details><summary>Hint 2: Approach</summary>

Get the Cloud Run URL from the deployment output or from GCP:
```bash
gcloud run services describe cloud-security-advisor --region=us-central1 --format='value(status.url)'
```

Open it in a browser. The app has a chat interface. You can also test from the command line using curl or the test script.

</details>

<details><summary>Hint 3: Implementation</summary>

Browser: Navigate to your Cloud Run URL and use the chat UI.

CLI testing:
```bash
# Using the test script
python scripts/test_inference.py --url <your-cloud-run-url>

# Or direct curl
curl -X POST <your-cloud-run-url>/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is the NIST Cybersecurity Framework?"}'
```

If the app returns errors, check:
1. Is the Vertex AI endpoint fully deployed? (Check the console)
2. Does the Cloud Run service account have `roles/aiplatform.user`?
3. Check Cloud Run logs: `gcloud run services logs read cloud-security-advisor --region=us-central1`

</details>

---

### Challenge 3.4: Explain the Architecture

This is the capstone challenge for Act 1. You have built a complete ML pipeline: train, merge, publish, deploy. Now prove you understand it.

Describe (to Claude, to a partner, or in notes) the full architecture. Cover:

1. **Where is the model?** -- Not in the Cloud Run container. It is loaded on a Vertex AI endpoint running a vLLM serving container on a GPU (g2-standard-12, 1x L4).

2. **Where is the app?** -- Cloud Run. A thin FastAPI service with 512MB RAM and no GPU. It handles authentication, chat templates, and proxies requests to the Vertex AI endpoint.

3. **How do they communicate?** -- The app calls Vertex AI's `rawPredict` API with an access token from `google.auth.default()`. The request goes to the vLLM container, which runs inference on the GPU and returns the completion.

4. **What artifacts flow through the pipeline?**
   - Gate 1: Base model + dataset --> LoRA adapter + manifest
   - Gate 2: Adapter + base model --> Merged model (safetensors) + updated manifest
   - Gate 3: Merged model --> Vertex AI endpoint + Cloud Run app

5. **What security scans happened between training and deployment?** -- None. (Yet.)

<details><summary>Hint 1: Concept</summary>

The key architectural insight is *separation of concerns*. The model (expensive GPU compute) is decoupled from the application (cheap CPU compute). This means you can update the app without redeploying the model, scale them independently, and -- critically -- insert security scan gates between pipeline stages.

</details>

<details><summary>Hint 2: Approach</summary>

Walk through each gate and describe what goes in and what comes out. Then trace a user request through the full system. Finally, identify where security checks *should* be (even though they are not there yet).

</details>

<details><summary>Hint 3: Implementation</summary>

Ask Claude to quiz you:

```
"Quiz me on the architecture. Ask me 5 questions about where the model lives, how requests flow, what artifacts exist at each gate, and what security checks are missing."
```

The critical gap to articulate: You just deployed a model to production without any security scanning. Anyone could have tampered with the base model, poisoned the training data, or injected malicious code into the artifacts. The pipeline works, but it is not secure. That is what Modules 4-7 will fix.

</details>

---

## Verification

Run `/verify-3` in Claude Code. The verification will:

- Confirm your Cloud Run application is live and responding to requests
- Confirm the Vertex AI endpoint is deployed and serving inference
- Confirm the application returns coherent cybersecurity-related responses
- Confirm you can explain why the model is not in the Cloud Run container
- Submit your progress to the leaderboard

## Customer Talking Points

- "This is a common enterprise architecture -- the model runs on GPU infrastructure, the application is a thin client. The security question every customer should ask: what scans happened between training and deployment? In most organizations, the answer is none."
- "Decoupled serving means you can scan and gate the model independently from the application code. The model never touches the app container -- it lives in a managed endpoint with its own access controls."
- "Gate-based pipelines give you audit points. At each gate, you can scan, verify provenance, and make go/no-go decisions. This is exactly where AIRS fits into the workflow."

---

## End of Act 1: Build It

Congratulations. You have built a complete ML pipeline from scratch:

**Train** (Gate 1) --> **Merge & Publish** (Gate 2) --> **Deploy** (Gate 3) --> **Live Application**

You understand:
- How models are trained (LoRA fine-tuning on Vertex AI)
- How adapters are merged into deployable artifacts (safetensors)
- How the serving architecture works (decoupled model + app)
- Where artifacts flow and how the pipeline chains together

**What is missing:** Security. No scans, no provenance verification, no malicious model detection. You deployed a model pulled from the public internet, trained on a public dataset, with zero security checks.

**What is next:** There is typically an instructor-led presentation between Modules 3 and 4 covering the AIRS value proposition, real-world model supply chain attacks, and customer scenarios. After that, Module 4 takes you deep into the AIRS product, and Modules 5-7 let you secure the pipeline you just built.

The transition question to carry into the next session: *"If someone published a malicious model on HuggingFace and your pipeline downloaded it, what would stop it from executing arbitrary code in your training infrastructure or on your GPU endpoint?"*

The answer, right now, is nothing. That is about to change.

## What's Next

**Presentation Break** -- Instructor-led session on AIRS value proposition, real incident case studies, and customer objection handling. Then Module 4: AIRS Deep Dive, where you will learn the scanning product inside and out before integrating it into this pipeline.

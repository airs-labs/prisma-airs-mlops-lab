# Module 3 Flow: Deploy & Serve

## Points Available

| Source | Points | Track |
|--------|--------|-------|
| App deployed (Cloud Run URL accessible) | 2 | All |
| App responds (health or chat works) | 2 | All |
| Understanding: decoupled architecture | 3 | All |
| Understanding: rawPredict and model naming | 3 | All |
| **Total** | **10** | |

---

## Challenge 3.1: Architecture First

### Flow

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

### Hints

**Hint 1 (Concept):** This is a *decoupled* architecture. The model runs on GPU infrastructure (Vertex AI endpoint with vLLM), and the application runs on lightweight infrastructure (Cloud Run with 512MB RAM). They communicate over an authenticated HTTP API. This separation means you can scale, update, and secure each component independently.

**Hint 2 (Approach):** Read three files to understand the architecture:
1. `src/airs_mlops_lab/serving/inference_client.py` -- the client that calls Vertex AI
2. `src/airs_mlops_lab/serving/server.py` -- the FastAPI application
3. `Dockerfile` -- what is (and is not) in the container

Trace a request from the user to the model and back.

**Hint 3 (Specific):** Ask Claude:

```
"Read inference_client.py and trace a chat request from the chat() method all the way to the Vertex AI endpoint. Explain the rawPredict call, the chat template formatting, and why we use model='openapi'."
```

Key architectural details:
- The app container has NO model weights, NO PyTorch, NO GPU -- just FastAPI + httpx + google-auth
- Auth uses `google.auth.default()` for access tokens (not identity tokens)
- Vertex AI's vLLM launcher overrides the served model name to "openapi" -- you must match this in requests
- The Vertex AI vLLM build only exposes `/v1/completions`, not `/v1/chat/completions` -- so the app constructs the chat template manually in the prompt

### Points: 0

---

## Challenge 3.2: Run the Pipeline

### Flow

Time to deploy. You will trigger Gate 2 (merge + publish) followed by Gate 3 (deploy endpoint + deploy app).

**Important context:** On the `lab-start` branch, there are NO AIRS scans in Gate 2 and NO manifest verification in Gate 3. The pipeline currently runs without any security checks. You will add those in Module 5.

Use `/explore deployment-pipeline` in Claude Code for guided exploration.

**Step 1: Trigger Gate 2** -- This merges your LoRA adapter with the base model and publishes the merged model to GCS.

**Step 2: Trigger Gate 3** -- This deploys the merged model to a Vertex AI endpoint (GPU) and deploys the application to Cloud Run.

### Hints

**Hint 1 (Concept):** Gate 2 takes the raw training output (adapter + base model) and produces a single merged model in safetensors format. Gate 3 takes the merged model, deploys it on a Vertex AI endpoint with a vLLM serving container, and deploys the Cloud Run application that talks to it. Deployment involves GPU provisioning, which takes 15-30 minutes.

**Hint 2 (Approach):** Use `gh workflow run` to trigger each gate. You will need to provide the correct input parameters -- particularly the `model_source` path from your Gate 1 training output. Check the workflow files or ask Claude what inputs each gate expects.

**Hint 3 (Specific):** Trigger Gate 2 (merge + publish):
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

### Points: 0

---

## Challenge 3.3: Test Your App

### Flow

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

### Hints

**Hint 1 (Concept):** The quality of responses depends on how many training steps you ran. With 50 steps, you will see some NIST influence but the model may still be generic in many areas. With 200+ steps, the cybersecurity specialization becomes more pronounced. This is the tradeoff between training cost and model quality.

**Hint 2 (Approach):** Get the Cloud Run URL from the deployment output or from GCP:
```bash
gcloud run services describe cloud-security-advisor --region=us-central1 --format='value(status.url)'
```

Open it in a browser. The app has a chat interface. You can also test from the command line using curl or the test script.

**Hint 3 (Specific):** Browser: Navigate to your Cloud Run URL and use the chat UI.

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

### Points: 0

---

## Challenge 3.4: Explain the Architecture

### Flow

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

### Hints

**Hint 1 (Concept):** The key architectural insight is *separation of concerns*. The model (expensive GPU compute) is decoupled from the application (cheap CPU compute). This means you can update the app without redeploying the model, scale them independently, and -- critically -- insert security scan gates between pipeline stages.

**Hint 2 (Approach):** Walk through each gate and describe what goes in and what comes out. Then trace a user request through the full system. Finally, identify where security checks *should* be (even though they are not there yet).

**Hint 3 (Specific):** Ask Claude to quiz you:

```
"Quiz me on the architecture. Ask me 5 questions about where the model lives, how requests flow, what artifacts exist at each gate, and what security checks are missing."
```

The critical gap to articulate: You just deployed a model to production without any security scanning. Anyone could have tampered with the base model, poisoned the training data, or injected malicious code into the artifacts. The pipeline works, but it is not secure. That is what Modules 4-7 will fix.

### Points: 0

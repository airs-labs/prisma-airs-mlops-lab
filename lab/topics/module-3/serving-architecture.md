# Serving Architecture

## Topics to Cover (in order)
1. Decoupled architecture -- model on Vertex AI GPU, app on Cloud Run (no GPU)
2. vLLM serving -- what it is, OpenAI-compatible API, why it matters for performance
3. rawPredict passthrough -- Vertex AI forwards requests directly to vLLM container
4. Chat template formatting -- Qwen2 `<|im_start|>` format, why model="openapi"
5. Why NOT /v1/chat/completions -- Vertex AI vLLM build only has /v1/completions

## Key Files
- `src/airs_mlops_lab/serving/inference_client.py` -- the client that calls Vertex AI
- `src/airs_mlops_lab/serving/server.py` -- the FastAPI app
- `Dockerfile` -- thin client, 512Mi RAM, no model in container

## How to Explore
- Read inference_client.py: trace a request from `chat()` to the Vertex AI endpoint
- Look at the Qwen2 chat template construction (lines 91-98)
- Read the Dockerfile: what is NOT in this container? Why?
- Compare: what would the container look like if the model was embedded?

## Student Activities
- Draw the request flow: user -> Cloud Run -> Vertex AI rawPredict -> vLLM -> response
- Why does the payload use `model: "openapi"` instead of the actual model name?
- What is the security benefit of keeping the model separate from the app container?

## Customer Talking Point
"Decoupled serving means you can scan and gate the model independently from the application code. The model never touches the app container -- it lives in a managed endpoint with its own access controls."

import os
import logging
from typing import List, Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("advisor-api")

# Global model state
model_resources = {}

class ChatRequest(BaseModel):
    message: str
    history: Optional[List[dict]] = None

class ChatResponse(BaseModel):
    reply: str
    metadata: dict

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load model on startup."""
    load_dotenv()
    mock_mode = os.getenv("MOCK_MODEL", "false").lower() == "true"
    
    if mock_mode:
        logger.info("🚧 MOCK_MODEL=true: Loading dummy model...")
        model_resources["mock"] = True
    else:
        logger.info("🤖 Loading LLM (Base + Adapter)...")
        try:
            from transformers import AutoModelForCausalLM, AutoTokenizer
            from peft import PeftModel
            import torch

            base_model_id = os.getenv("BASE_MODEL", "Qwen/Qwen2.5-3B-Instruct")
            adapter_path = os.getenv("ADAPTER_PATH", "models/final_adapter")

            # Load Tokenizer
            tokenizer = AutoTokenizer.from_pretrained(base_model_id, trust_remote_code=True)
            
            # Load Base Model
            logger.info(f"Loading base: {base_model_id}")
            base_model = AutoModelForCausalLM.from_pretrained(
                base_model_id,
                torch_dtype=torch.float16,
                device_map="auto",
                trust_remote_code=True
            )

            # Load Adapter (if exists)
            if os.path.exists(adapter_path):
                logger.info(f"Loading adapter: {adapter_path}")
                model = PeftModel.from_pretrained(base_model, adapter_path)
            else:
                logger.warning(f"Adapter not found at {adapter_path}. Using base model.")
                model = base_model

            model_resources["model"] = model
            model_resources["tokenizer"] = tokenizer
            model_resources["mock"] = False
            logger.info("✅ Model loaded successfully")
            
        except Exception as e:
            logger.error(f"❌ Failed to load model: {e}")
            logger.warning("Falling back to MOCK mode due to error.")
            model_resources["mock"] = True

    yield
    # Cleanup resources
    model_resources.clear()

app = FastAPI(title="Cloud Security Advisor API", lifespan=lifespan)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static frontend
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "mode": "mock" if model_resources.get("mock") else "inference"
    }

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Generate a response from the Advisor."""
    if model_resources.get("mock"):
        # Mock logic for testing UI/Pipeline
        import time
        time.sleep(1.0) # Simulate latency
        return ChatResponse(
            reply=f"MOCK ADVISOR ALERT: I received your message: '{request.message}'. "
                  "Since I am running in mock mode, I cannot give real security advice, "
                  "but I can confirm the pipeline is working!",
            metadata={"model": "mock-v1", "steps": 0}
        )

    # Real Inference
    try:
        model = model_resources["model"]
        tokenizer = model_resources["tokenizer"]
        
        # Format messages (simple history handling could be added here)
        messages = [
            {"role": "system", "content": "You are a helpful cloud security advisor."},
            {"role": "user", "content": request.message}
        ]
        
        text = tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
        
        inputs = tokenizer([text], return_tensors="pt").to(model.device)
        
        outputs = model.generate(
            **inputs,
            max_new_tokens=256,
            temperature=0.7,
            do_sample=True 
        )
        
        generated_ids = [
            output_ids[len(input_ids):] for input_ids, output_ids in zip(inputs.input_ids, outputs)
        ]
        response_text = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
        
        return ChatResponse(
            reply=response_text,
            metadata={"model": "qwen-advisor", "tokens": len(generated_ids[0])}
        )
        
    except Exception as e:
        logger.error(f"Inference error: {e}")
        raise HTTPException(status_code=500, detail="Inference failed")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)

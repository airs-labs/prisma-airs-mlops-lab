#!/usr/bin/env python3
"""
Cloud Security Advisor - Interactive Chat

Test the fine-tuned Cloud Security Advisor model by chatting with it.
Supports both:
- Base model + LoRA adapters (default)
- Merged model

Usage:
    python chat.py                                    # Use default adapter path
    python chat.py --adapter-path models/my-adapter   # Custom adapter
    python chat.py --merged-model models/merged       # Use merged model
    python chat.py --question "What is NIST 800-53?"  # Single question mode
"""

import argparse
import json
from pathlib import Path

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import PeftModel
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

console = Console()

# Default paths
DEFAULT_BASE_MODEL = "microsoft/Phi-3-mini-4k-instruct"
DEFAULT_ADAPTER_PATH = "models/cloud-security-advisor/final_adapter"

# System prompt for the advisor
SYSTEM_PROMPT = """You are a cybersecurity expert with deep knowledge of NIST standards, frameworks, and best practices. You provide accurate, detailed guidance on cybersecurity controls, risk management, cloud security, and compliance based on NIST publications including the 800 series, FIPS, and related documents."""


def load_model(
    base_model_id: str = DEFAULT_BASE_MODEL,
    adapter_path: str = None,
    merged_model_path: str = None,
    use_4bit: bool = True,
):
    """Load the model for inference."""
    
    if merged_model_path:
        console.print(f"[bold blue]🤖 Loading merged model from: {merged_model_path}[/bold blue]")
        
        tokenizer = AutoTokenizer.from_pretrained(merged_model_path)
        model = AutoModelForCausalLM.from_pretrained(
            merged_model_path,
            device_map="auto",
            torch_dtype=torch.bfloat16,
        )
    else:
        console.print(f"[bold blue]🤖 Loading base model: {base_model_id}[/bold blue]")
        
        # Quantization for inference
        if use_4bit:
            bnb_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_use_double_quant=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_compute_dtype=torch.bfloat16,
            )
        else:
            bnb_config = None
        
        tokenizer = AutoTokenizer.from_pretrained(base_model_id, trust_remote_code=True)
        model = AutoModelForCausalLM.from_pretrained(
            base_model_id,
            quantization_config=bnb_config,
            device_map="auto",
            trust_remote_code=True,
        )
        
        # Load LoRA adapter if provided
        if adapter_path and Path(adapter_path).exists():
            console.print(f"[bold blue]🔧 Loading LoRA adapter: {adapter_path}[/bold blue]")
            model = PeftModel.from_pretrained(model, adapter_path)
        elif adapter_path:
            console.print(f"[yellow]⚠️ Adapter path not found: {adapter_path}[/yellow]")
            console.print("[yellow]Running with base model only[/yellow]")
    
    # Set padding token
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    
    model.eval()
    console.print("[green]✅ Model loaded successfully![/green]\n")
    
    return model, tokenizer


def generate_response(
    model,
    tokenizer,
    user_message: str,
    history: list = None,
    max_new_tokens: int = 512,
    temperature: float = 0.7,
):
    """Generate a response to the user's message."""
    
    # Build conversation
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    
    if history:
        messages.extend(history)
    
    messages.append({"role": "user", "content": user_message})
    
    # Apply chat template
    prompt = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )
    
    # Tokenize
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    
    # Generate
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            temperature=temperature,
            do_sample=temperature > 0,
            pad_token_id=tokenizer.pad_token_id,
            eos_token_id=tokenizer.eos_token_id,
        )
    
    # Decode only the new tokens
    input_length = inputs["input_ids"].shape[1]
    response = tokenizer.decode(
        outputs[0][input_length:],
        skip_special_tokens=True
    )
    
    return response.strip()


def chat_loop(model, tokenizer):
    """Interactive chat loop."""
    
    console.print(Panel.fit(
        "[bold green]Cloud Security Advisor[/bold green]\n"
        "Ask questions about NIST standards and cloud security best practices.\n"
        "Type 'quit' or 'exit' to end the session.\n"
        "Type 'clear' to reset conversation history.",
        title="🔒 Security Advisor"
    ))
    
    history = []
    
    while True:
        try:
            user_input = console.input("\n[bold cyan]You:[/bold cyan] ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ["quit", "exit", "q"]:
                console.print("[dim]Goodbye![/dim]")
                break
            
            if user_input.lower() == "clear":
                history = []
                console.print("[dim]Conversation history cleared.[/dim]")
                continue
            
            # Generate response
            console.print("\n[bold green]Advisor:[/bold green] ", end="")
            
            with console.status("[bold yellow]Thinking...[/bold yellow]"):
                response = generate_response(
                    model, tokenizer,
                    user_input,
                    history=history
                )
            
            # Display response as markdown
            console.print(Markdown(response))
            
            # Update history
            history.append({"role": "user", "content": user_input})
            history.append({"role": "assistant", "content": response})
            
            # Keep history manageable
            if len(history) > 10:
                history = history[-10:]
                
        except KeyboardInterrupt:
            console.print("\n[dim]Interrupted. Goodbye![/dim]")
            break


def main():
    parser = argparse.ArgumentParser(description="Chat with Cloud Security Advisor")
    parser.add_argument("--base-model", type=str, default=DEFAULT_BASE_MODEL,
                        help="Base model ID")
    parser.add_argument("--adapter-path", type=str, default=DEFAULT_ADAPTER_PATH,
                        help="Path to LoRA adapter")
    parser.add_argument("--merged-model", type=str, default=None,
                        help="Path to merged model (overrides base + adapter)")
    parser.add_argument("--no-4bit", action="store_true",
                        help="Disable 4-bit quantization")
    parser.add_argument("--question", "-q", type=str, default=None,
                        help="Ask a single question (non-interactive mode)")
    
    args = parser.parse_args()
    
    # Load model
    model, tokenizer = load_model(
        base_model_id=args.base_model,
        adapter_path=args.adapter_path,
        merged_model_path=args.merged_model,
        use_4bit=not args.no_4bit,
    )
    
    if args.question:
        # Single question mode
        console.print(f"\n[bold cyan]Question:[/bold cyan] {args.question}")
        console.print(f"\n[bold green]Advisor:[/bold green]")
        
        response = generate_response(model, tokenizer, args.question)
        console.print(Markdown(response))
    else:
        # Interactive mode
        chat_loop(model, tokenizer)


if __name__ == "__main__":
    main()

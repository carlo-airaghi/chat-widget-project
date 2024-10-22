# app.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import os

app = FastAPI()

class GenerateRequest(BaseModel):
    prompt: str
    max_length: int = 512
    temperature: float = 0.7

# Load the model and tokenizer from the local path
model_name = os.getenv("MODEL_NAME", "EleutherAI/gpt-neo-125M")
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

try:
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
        device_map="auto",
    )
except Exception as e:
    raise RuntimeError(f"Error loading model: {e}")

@app.post("/generate")
def generate_text(request: GenerateRequest):
    prompt = request.prompt
    max_length = request.max_length
    temperature = request.temperature

    try:
        input_ids = tokenizer.encode(prompt, return_tensors="pt").to(device)
        output = model.generate(
            input_ids,
            max_length=max_length,
            temperature=temperature,
            do_sample=True,
            top_p=0.95,
            pad_token_id=tokenizer.eos_token_id,
        )
        generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
        # Remove the prompt from the generated text
        generated_text = generated_text[len(prompt):].strip()
        return {"generated_text": generated_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

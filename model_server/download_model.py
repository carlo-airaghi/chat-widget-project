# download_model.py
import os
from transformers import AutoModelForCausalLM, AutoModelForMaskedLM, AutoTokenizer

model_name = os.getenv('MODEL_NAME')
model_type = os.getenv('MODEL_TYPE')

if not model_name or not model_type:
    raise ValueError('MODEL_NAME and MODEL_TYPE must be set')

tokenizer = AutoTokenizer.from_pretrained(model_name)

if model_type == 'causal':
    AutoModelForCausalLM.from_pretrained(model_name)
elif model_type == 'masked':
    AutoModelForMaskedLM.from_pretrained(model_name)
else:
    raise ValueError('Invalid MODEL_TYPE')

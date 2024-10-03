import os
from transformers import AutoModelForCausalLM, AutoModelForMaskedLM, AutoTokenizer

model_name = os.getenv('MODEL_NAME').strip()
model_type = os.getenv('MODEL_TYPE').strip()

if not model_name or not model_type:
    raise ValueError('MODEL_NAME and MODEL_TYPE must be set')

tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.save_pretrained('./model')

if model_type == 'causal':
    model = AutoModelForCausalLM.from_pretrained(model_name)
elif model_type == 'masked':
    model = AutoModelForMaskedLM.from_pretrained(model_name)
else:
    raise ValueError('Invalid MODEL_TYPE')

model.save_pretrained('./model')

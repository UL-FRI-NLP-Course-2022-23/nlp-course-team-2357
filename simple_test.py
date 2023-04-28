import torch
from transformers import (
    T5ForConditionalGeneration,
    T5Tokenizer,
)

model_id = 'Paraphrase_generator'
model = T5ForConditionalGeneration.from_pretrained(model_id)
#model = MT5ForConditionalGeneration.from_pretrained(model_id)
tokenizer = T5Tokenizer.from_pretrained('cjvt/t5-sl-small')

device = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"
model = model.to(device)

def generate(text,model,tokenizer):
   model.eval()
   input_ids = tokenizer.encode(text,return_tensors="pt").to(device)  
   outputs = model.generate(input_ids,max_new_tokens=1000,min_new_tokens=100)
   return tokenizer.decode(outputs[0])

inp = "Danes je zunaj lep sončen dan. Na nebu ni niti enega oblaka"

print(generate(inp,model,tokenizer))

import torch
from transformers import (
    T5ForConditionalGeneration,
    T5Tokenizer,
)

model = T5ForConditionalGeneration.from_pretrained('Paraphrase_generator')
#model = MT5ForConditionalGeneration.from_pretrained(model_id)
tokenizer = T5Tokenizer.from_pretrained('cjvt/t5-sl-small')

device = "cuda" if torch.cuda.is_available() else "cpu"
model = model.to(device)

def generate(text, model, tokenizer, method="greedy", num_outputs=3, evaluating=False):
    """
    Feel free to play around with temperature, top_k and top_p values
    """
    model.eval()
    input_ids = tokenizer.encode(text, return_tensors="pt").to(device)

    beams = 5
    temperature = 0.7
    top_k = 50
    top_p = 0.95

    if method == "greedy":
        outputs = model.generate(input_ids, max_new_tokens=1000)
    elif method == "beam":
        outputs = model.generate(input_ids,
                                 max_new_tokens=1000, 
                                 num_beams=beams,
                                 early_stopping=True,
                                 num_return_sequences=min(num_outputs, beams),
                                 # no_repeat_ngram_size=3,
                                 )
    elif method == "sample":
        outputs = model.generate(input_ids,
                                 max_new_tokens=1000,
                                 do_sample=True,
                                 temperature=temperature,
                                 top_k=0,
                                 num_return_sequences=num_outputs,
                                 )
    elif method == "top_k":
        outputs = model.generate(input_ids,
                                 max_new_tokens=1000,
                                 do_sample=True,
                                 temperature=temperature,
                                 top_k=top_k,
                                 num_return_sequences=num_outputs,
                                 )
    elif method == "top_p":
        outputs = model.generate(input_ids,
                                 max_new_tokens=1000,
                                 do_sample=True,
                                 temperature=temperature,
                                 top_p=top_p,
                                 top_k=top_k,
                                 num_return_sequences=num_outputs,
                                 )
        
    if not evaluating:
        for i, output in enumerate(outputs):
            print(f"{i+1}: {tokenizer.decode(output, skip_special_tokens=True)}")
        print("-" * 100)
        print()
    else:
        return tokenizer.decode(outputs[0], skip_special_tokens=True)

def main():
    inp = "Choose output generation method (greedy, beam, sample, top_k, top_p)\n"
    method = input(inp)
    print()

    inp = "Please enter the message, or 'exit' to exit\n"
    data = input(inp)
    print("-" * 100)

    while 'exit' != data:
        generate(data, model, tokenizer, method=method)
        data = input(inp)
        print("-" * 100)


if __name__ == "__main__":
    main()

import os
import torch
from transformers import (
    T5ForConditionalGeneration,
    T5Tokenizer,
)

from simple_test import generate
from datasets import load_metric

PATH_TO_INPUT = "cckres/preprocessed"
PATH_TO_REFERENCE = "cckres/translated/sl"

model = T5ForConditionalGeneration.from_pretrained('Paraphrase_generator')
#model = MT5ForConditionalGeneration.from_pretrained(model_id)
tokenizer = T5Tokenizer.from_pretrained('cjvt/t5-sl-small')

device = "cuda" if torch.cuda.is_available() else "cpu"
model = model.to(device)

rouge = load_metric("rouge")
sacrebleu = load_metric("sacrebleu")


def main():
    predictions = []
    references = []
    inp = "Choose output generation method (greedy, beam, sample, top_k, top_p)\n"
    method = input(inp)
    all_files = os.listdir(PATH_TO_INPUT)
    for filename in all_files:
        f = os.path.join(PATH_TO_INPUT, filename)
        with open(f, encoding='utf-8') as f:
            contents = f.read()
            lines = contents.split('\n')[:-1]
            for data in lines:
                predictions.append(generate(data, model, tokenizer, method=method, num_outputs=1, evaluating=True))

        f = os.path.join(PATH_TO_REFERENCE, filename)
        with open(f, encoding='utf-8') as f:
            contents = f.read()
            lines = contents.split('\n')[:-1]
            for data in lines:
                references.append([data])
        break

    print(rouge.compute(predictions=predictions, references=references))
    print(sacrebleu.compute(predictions=predictions, references=references))

if __name__ == "__main__":
    main()
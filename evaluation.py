
import os
import json
import torch
import evaluate
from transformers import (
    T5ForConditionalGeneration,
    T5Tokenizer,
)
from tqdm import tqdm

from simple_test import generate


# PATH_TO_INPUT - path to files containing input sentences for the paraphrasing model
# PATH_TO_REFERENCE - path to files with reference paraphrases ("ground truths" for the input)
PATH_TO_INPUT = "evaluation_ccgiga_final/preprocessed"
PATH_TO_REFERENCE = "evaluation_ccgiga_final/translated"

model = T5ForConditionalGeneration.from_pretrained("./t5-large-2")
tokenizer = T5Tokenizer.from_pretrained(f'cjvt/t5-sl-large')  # t5-sl-small and t5-sl-large tokenizer are the same
print("Model and tokenizer loaded")

device = "cuda" if torch.cuda.is_available() else "cpu"
model = model.to(device)

rouge = evaluate.load("rouge")
bleu = evaluate.load("bleu")

def main():
    predictions = []
    references = []
    # inp = "Choose output generation method (greedy, beam, sample, top_k, top_p)\n"
    # method = input(inp)
    method = "top_k"
    all_files = os.listdir(PATH_TO_INPUT)
    for filenum, filename in enumerate(all_files):
        f = os.path.join(PATH_TO_INPUT, filename)
        with open(f, encoding='utf-8') as f:
            contents = f.read()
            lines = contents.split('\n')[:-1]
            for data in tqdm(lines, desc=f"File {filename}, {filenum+1}/{len(all_files)}", ncols=100):
                predictions.append(generate(data, model, tokenizer, method=method, num_outputs=1, evaluating=True))

        f = os.path.join(PATH_TO_REFERENCE, filename)
        with open(f, encoding='utf-8') as f:
            contents = f.read()
            lines = contents.split('\n')[:-1]
            for data in lines:
                references.append([data])

    print()
    print("ROUGE:", json.dumps(rouge.compute(predictions=predictions, references=references), indent=4))
    print("BLEU:", json.dumps(bleu.compute(predictions=predictions, references=references), indent=4))

if __name__ == "__main__":
    main()
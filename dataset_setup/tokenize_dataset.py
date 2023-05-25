import os
from transformers import AutoTokenizer
from datasets import Dataset


# DATASET is one of "cckres", "ccgiga"
# ROOT_DIR is the path to translated_cckres i.e. translated_ccgiga:
# the raw dataset containing the preprocessed and back-translated documents
DATASET = "cckres"
ROOT_DIR = f"../translated_{DATASET}"


def main():

    def preprocess_function(original, translated):
        # Maximum length of the tokenized sentence. 99% of all documents from translated_cckres
        # and translated_ccgiga will be tokenized to <= 128 tokens.
        max_len = 128
        model_inputs = tokenizer(original, max_length=max_len, truncation=True)

        # Setup the tokenizer for targets
        with tokenizer.as_target_tokenizer():
            labels = tokenizer(translated, max_length=max_len, truncation=True)

        model_inputs["labels"] = labels["input_ids"]
        return model_inputs
    
    # Directory to save results
    tokenized_dir = "../tokenized"
    if not os.path.exists(tokenized_dir):
        os.mkdir(tokenized_dir)

    print("Loading the tokenizer")
    tokenizer = AutoTokenizer.from_pretrained("cjvt/t5-sl-large")  # tokenizer is same as for t5-sl-small
    print("Tokenizer successfully loaded")

    preprocessed_dir = f"{ROOT_DIR}/preprocessed"
    translated_dir = f"{ROOT_DIR}/translated/sl"
    original = []
    translated = []
    
    print("Fetching sentence pairs")
    files = os.listdir(preprocessed_dir)
    for i, name in enumerate(files):
        if (i + 1) % 1000 == 0:
            print(f"At file {i + 1} / {len(files)}")

        preprocessed_file = f"{preprocessed_dir}/{name}"
        translated_file = f"{translated_dir}/{name}"
        
        with open(preprocessed_file, "r", encoding="utf8") as pf:
            preprocessed_contents = pf.read()

        with open(translated_file, "r", encoding="utf8") as sf:
            translated_contents = sf.read()

        # Get sentences (one sentence per line)
        preprocessed_lines = preprocessed_contents.split("\n")[:-1]
        translated_lines = translated_contents.split("\n")[:-1]

        original += preprocessed_lines
        translated += translated_lines
    
    # Split paraphrase pairs in batches of 500000, tokenize and save
    counter = 1
    constant = 500000
    while True:
        original_batch = original[(counter-1) * constant:counter * constant]
        translated_batch = translated[(counter-1) * constant:counter * constant]
        json_name = f"{tokenized_dir}/{DATASET}_tokenized_{counter}.json"

        print(f"Preprocessing {json_name}")
        tokenized = preprocess_function(original_batch, translated_batch)
        tokenized = Dataset.from_dict(tokenized)
        tokenized.to_json(json_name)
        print(f"Saved {json_name}\n")

        counter += 1
        if len(original_batch) < constant:
            # This is the last batch, since it doesn't have `constant` sentences.
            break

    print("Dataset successfully tokenized")
              
if __name__ == '__main__':
    main()
    
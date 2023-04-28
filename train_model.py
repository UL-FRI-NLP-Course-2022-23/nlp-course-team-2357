def main():

    from torch.utils.data import Dataset
    import torch
    import os
    from transformers import AutoModelForSeq2SeqLM, DataCollatorForSeq2Seq, Seq2SeqTrainingArguments, Seq2SeqTrainer, AutoTokenizer
    from datasets import Dataset


    def preprocess_function(original,translated):

        max_input_length = 64
        max_target_length = 16

        model_inputs = tokenizer(original, max_length=max_input_length, truncation=True)

        # Setup the tokenizer for targets
        with tokenizer.as_target_tokenizer():
            labels = tokenizer(translated, max_length=max_target_length, truncation=True)

        model_inputs["labels"] = labels["input_ids"]
        return model_inputs
    
    device = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"

    tokenizer = AutoTokenizer.from_pretrained("cjvt/t5-sl-small")
    model = AutoModelForSeq2SeqLM.from_pretrained("cjvt/t5-sl-small")


    model = model.to(device)

    listdir = "cckres/preprocessed"
    listdir1 = "cckres/translated/sl"
    original = []
    translated = []

    cc = 0
    for preprocessed_name, slovene_name in zip(os.listdir(listdir), os.listdir(listdir1)):

        preprocessed_file = f"{listdir}/{preprocessed_name}"
        slovene_file = f"{listdir1}/{slovene_name}"
        
        with open(preprocessed_file, "r", encoding="utf8") as pf:
            preprocessed_contents = pf.read()

        with open(slovene_file, "r", encoding="utf8") as sf:
            slovene_contents = sf.read()

        preprocessed_lines = preprocessed_contents.split("\n")[:-1]
        slovene_lines = slovene_contents.split("\n")[:-1]

        if len(preprocessed_lines) != len(slovene_lines):
            cc = cc + 1
            continue

        original += preprocessed_lines
        translated += slovene_lines

    print(cc)
    if len(original) == len(translated):
        print("WE DID IT!")
        print(len(original))
        print(len(translated))
    else:
        print("Oh no size missmatched")
        print(len(original))
        print(len(translated))

    tokenized_datasets = preprocess_function(original,translated)
    tokenized_datasets = Dataset.from_dict(tokenized_datasets)

    batch_size = 16
    args = Seq2SeqTrainingArguments(
        f"Paraphrase_generator",
        #evaluation_strategy = "epoch",
        learning_rate=2e-5,
        per_device_train_batch_size=batch_size,
        #per_device_eval_batch_size=batch_size,
        weight_decay=0.01,
        save_total_limit=3,
        num_train_epochs=1,
        predict_with_generate=True,
        fp16=False,
        #push_to_hub=True,
    )

    data_collator = DataCollatorForSeq2Seq(tokenizer, model=model)

    trainer = Seq2SeqTrainer(
        model,
        args,
        train_dataset=tokenized_datasets,
        data_collator=data_collator,
        tokenizer=tokenizer
    )
    if __name__ == '__main__':
        trainer.train()
        trainer.model.save_pretrained('Paraphrase_generator')
              
if __name__ == '__main__':
    main()    

import datasets
import torch
from transformers import AutoModelForSeq2SeqLM, DataCollatorForSeq2Seq, Seq2SeqTrainingArguments, Seq2SeqTrainer, AutoTokenizer

def main():
    
    device = "cuda" if torch.cuda.is_available() else "cpu"
    tokenizer = AutoTokenizer.from_pretrained("cjvt/t5-sl-small")
    model = AutoModelForSeq2SeqLM.from_pretrained("cjvt/t5-sl-small")
    model = model.to(device)
    print("Model and tokenizer loaded")

    tokenized_dataset = datasets.Dataset.from_json("tokenized/cckres_tokenized_1.json")

    batch_size = 64
    args = Seq2SeqTrainingArguments(
        f"ccKres_5_epoch",  # directory where it saves checkpoints after each epoch
        learning_rate=2e-5,
        per_device_train_batch_size=batch_size,
        #per_device_eval_batch_size=batch_size,
        weight_decay=0.01,
        #save_total_limit=3,
        num_train_epochs=5,
        predict_with_generate=True,
        fp16=False,
        save_strategy="epoch"
        #push_to_hub=True,
    )

    data_collator = DataCollatorForSeq2Seq(tokenizer, model=model)

    trainer = Seq2SeqTrainer(
        model,
        args,
        train_dataset=tokenized_dataset,
        data_collator=data_collator,
        tokenizer=tokenizer
    )
    if __name__ == '__main__':
        trainer.train()
        trainer.model.save_pretrained('ccKres_5_epoch')  # also a directory
              
if __name__ == '__main__':
    main()

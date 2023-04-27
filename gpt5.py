def main():

    from transformers import GPT2LMHeadModel, GPT2Tokenizer
    from torch.optim import Adam
    from torch.utils.data import DataLoader
    import tqdm
    from torch.utils.data import Dataset, DataLoader
    import torch
    import pandas as pd
    import os
    from transformers import AutoTokenizer, AutoModelForCausalLM
    #from pynvml import *

    from transformers import AutoModelForSeq2SeqLM, DataCollatorForSeq2Seq, Seq2SeqTrainingArguments, Seq2SeqTrainer
    from transformers import (
        AdamW,
        T5ForConditionalGeneration,
        T5Tokenizer,
        get_linear_schedule_with_warmup
    )
    from transformers import TrainingArguments, Trainer, logging
    from datasets import Dataset


    #---------------------
    class ChatData(Dataset):
        def __init__(self, tokenizer):
            #self.data = json.load(open(path, "r"))
            
            #----------
            listdir = "cckres/translated/sl"
            listdir1 = "cckres/preprocessed"
            self.X = []
            self.original = []
            i=0
            for filename in os.listdir(listdir1):
                f = os.path.join("cckres/preprocessed", filename)       
                        
                if os.path.isfile(f):
                    with open(f, encoding='utf-8') as f:
                        while f.readline():
                            temp = f.readline()
                            if len(temp) > 6:
                                #self.X.append(temp)
                                self.original.append(temp)
                                #writer.writerow([temp],["test"])
                                #writer.writerow(['abc','cba'])
                                #writer.writerow(['']+[["test"]])
                    i = i + 1
                    if i > 100:
                        break

            i = 0
            self.translated = [] 
            for filename in os.listdir(listdir):
                f = os.path.join("cckres/translated/sl", filename)       
                        
                if os.path.isfile(f):
                    with open(f, encoding='utf-8') as f:
                        while f.readline():
                            temp = f.readline()
                            if len(temp) > 6:
                                self.translated.append(temp)
                    i = i + 1
                    if i > 100:
                        break
            #-------------

            # for idx, i in enumerate(self.X):
            #     try:
            #         self.X[idx] = "<startofstring> "+i+" <bot>: "+self.translated[idx]+" <endofstring>"
            #     except:
            #         break

            #self.X = self.X[:5000]
            
            print(self.original[0])
            print(len(self.original))

            self.X_encoded = tokenizer(self.original,max_length=40, truncation=True, padding="max_length", return_tensors="pt")
            #print(self.X_encoded[0])
            self.input_ids = self.X_encoded['input_ids']
            self.attention_mask = self.X_encoded['attention_mask']

            # Setup the tokenizer for targets
            self.X_encoded_label = tokenizer(self.translated, max_length=40, truncation=True, padding="max_length", return_tensors="pt")
            #self.X_encoded = tokenizer(self.translated,max_length=40, truncation=True, padding="max_length", return_tensors="pt")
            #self.label = self.X_encoded['label']
            self.labels = self.X_encoded_label['input_ids']
            #print(self.labels[0])

        def __len__(self):
            return len(self.original)

        def __getitem__(self, idx):
            return (self.input_ids[idx], self.attention_mask[idx], self.labels[idx])




    def train(chatData, model, optim):

        epochs = 6

        for i in tqdm.tqdm(range(epochs)):
            for X, a in chatData:
                X = X.to(device)
                a = a.to(device)
                optim.zero_grad()
                loss = model(X, attention_mask=a, labels=X).loss
                loss.backward()
                optim.step()
            torch.save(model.state_dict(), "model_state.pt")
            #print(infer("hello how are you"))

    def infer(inp):
        inp = "<startofstring> "+inp+" <bot>: "
        inp = tokenizer(inp, return_tensors="pt")
        X = inp["input_ids"].to(device)
        a = inp["attention_mask"].to(device)
        output = model.generate(X, attention_mask=a )
        output = tokenizer.decode(output[0])
        return output


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

    tokenizer = AutoTokenizer.from_pretrained("cjvt/t5-sl-large")
    #tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    #tokenizer.add_special_tokens({"pad_token": "<pad>", 
    #                                "bos_token": "<startofstring>",
    #                                "eos_token": "<endofstring>"})
    #tokenizer.add_tokens(["<bot>:"])

    model = AutoModelForSeq2SeqLM.from_pretrained("cjvt/t5-sl-large")
    #model.resize_token_embeddings(len(tokenizer))

    model = model.to(device)

    #----------
    listdir = "cckres/translated/sl"
    listdir1 = "cckres/preprocessed"
    original = []

    i=0
    for filename in os.listdir(listdir1):
        f = os.path.join("cckres/preprocessed", filename)       
                
        if os.path.isfile(f):
            with open(f, encoding='utf-8') as f:
                while f.readline():
                    temp = f.readline()
                    if len(temp) > 6:
                        #self.X.append(temp)
                        original.append(temp)
                        #writer.writerow([temp],["test"])
                        #writer.writerow(['abc','cba'])
                        #writer.writerow(['']+[["test"]])
                        i = i + 1
                        if i > 100:
                            break

    i = 0
    translated = [] 
    for filename in os.listdir(listdir):
        f = os.path.join("cckres/translated/sl", filename)       
                
        if os.path.isfile(f):
            with open(f, encoding='utf-8') as f:
                while f.readline():
                    temp = f.readline()
                    if len(temp) > 6:
                        i = i + 1
                        if i > len(original):
                            break
                        translated.append(temp)
                        
    #-------------

    #print(len(original))
    #print(len(translated))

    #dataset = ChatData(tokenizer)
    #print(dataset[0])

    # print(tokenizer.decode(model.generate(**tokenizer("hey i was good at basketball but ",
    #                          return_tensors="pt"))[0]))

    #tokenized_datasets = map(preprocess_function(original,translated), batched=True)
    tokenized_datasets = preprocess_function(original,translated)
    tokenized_datasets = Dataset.from_dict(tokenized_datasets)
    #print(type(tokenized_datasets))

    batch_size = 8
    model_name = "fine-tune"

    args = Seq2SeqTrainingArguments(
        f"{model_name}-finetuned-xsum",
        num_train_epochs=1,
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        eval_accumulation_steps=1,
        learning_rate=0.001,
        evaluation_strategy='steps',
        save_steps=1000000,
        save_total_limit=1,
        remove_unused_columns=True,
        logging_steps=100,
        eval_steps=100,
        logging_first_step=True
    )



    #tokenized_datasets = dataset.map(dataset, batched=True)


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
              
if __name__ == '__main__':
    main()    

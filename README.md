# Natural language processing course 2022/23: Paraphrasing sentences <!-- omit in toc -->

Team members:
 * Mitja Vendramin, 63170301, mv2825@student.uni-lj.si
 * Luka Boljević, 63210482, lb7093@student.uni-lj.si
 * Matjaž Bizjak, 63170054, mb0539@student.uni-lj.si
 
Group public acronym/name: nlp-course-team-2357



# Table of contents <!-- omit in toc -->

- [Dataset](#dataset)
- [Slovene NMT](#slovene-nmt)
  - [Setup and usage](#setup-and-usage)
- [Model training](#model-training)
  - [Testing the model](#testing-the-model)



# Dataset

For this project, our main datasets are [ccKres](https://www.clarin.si/repository/xmlui/handle/11356/1034) and [ccGigafida](https://www.clarin.si/repository/xmlui/handle/11356/1035). Some basic info and statistics can be found in the report, and you can also read more about ccKres, ccGigafida, and open Slovene corpora in general on [this link](http://eng.slovenscina.eu/korpusi/proste-zbirke).

The dataset we used to train the models for paraphrasing can be found [on this OneDrive link](https://unilj-my.sharepoint.com/personal/slavkozitnik_fri1_uni-lj_si/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fslavkozitnik%5Ffri1%5Funi%2Dlj%5Fsi%2FDocuments%2FFRI%2FNLP%5FCourse%5F2023%2FProjects%20data%20to%20share&ga=1), in the folder "Sentence paraphrasing (Team 2357)". There, you will find an accompanying README, where we explain how we obtained the dataset for training.

All scripts related to working with the dataset (downloading, preprocessing, back-translation and tokenizing) can be found in the `dataset_setup` folder. However, it is not necessary to run any of them, as we suggest just downloading everything from the OneDrive link above (if need be).



# Slovene NMT

For back-translation, we used the [Slovene_NMT](https://github.com/clarinsi/Slovene_NMT) Neural Machine Translator. Unless you want to play around with it, or rebuild the training data we used from scratch, you don't need to set it up, and you can freely skip the following subsection.


## Setup and usage

If you want to set it up, first install Docker on your machine (if not already), and run one of the setup scripts found in `nmt_files`. There are 3 scripts there - one for Linux users, and two for Windows users, based on which terminal you prefer using (Git Bash or PowerShell). All scripts accept arguments `cpu` and `gpu` - `cpu` should be used if you want to deploy Slovene NMT on the CPU, and `gpu` if you want to deploy on an NVIDIA GPU. Open the scripts for more details.

If you are on Linux, run the linux script, namely [`setup_translator_linux.sh`](nmt_files/setup_translator_linux.sh). If you are on Windows, and use Git Bash, run [`setup_translator_gitbash.sh`](nmt_files/setup_translator_gitbash.sh). If you are on Windows, and prefer using PowerShell, run [`setup_translator_powershell.ps1`](nmt_files/setup_translator_powershell.ps1) (make sure to run PowerShell as **Administrator** first).

Please keep in mind that downloading the NVIDIA models via PowerShell is rather slow. If you want, you can manually download and place the NVIDIA models in the appropriate directory inside `Slovene_NMT`, and comment out unnecessary commands in the script.

Note that the API of the two containers will not be available until the model is loaded inside the container, which can take about 6 to 7 minutes. It is best to stream the logs with `docker logs -f translator_slen` i.e. `docker logs -f translator_ensl` and see exactly when the initialization finishes. 

After it finishes, the API will be available on `localhost` ports 4001 (English to Slovene translation) and 4002 (Slovene to English translation). Check the file [`SloveneNMT_example_usage.md`](nmt_files/SloveneNMT_example_usage.md) for details how to use the API.

**Important note**: on Windows, the two Docker containers that will be created, coupled with the VM Docker Desktop uses in the background, can in total easily take up 12-13GB of RAM just to be able to run. If you have more than 16GB of RAM, you should be okay, but if you don't, we **strongly** suggest running one container at a time.

Setting up `Slovene_NMT` can also be done "manually". The steps can be found in [`SloveneNMT_manual_setup.md`](nmt_files/SloveneNMT_manual_setup.md).



# Model training

As our base model, we chose models pretrained on Slovene from [cjvt repository](https://huggingface.co/cjvt) on HuggingFace. TODO We fine tuned both [`t5-sl-small`](https://huggingface.co/cjvt/t5-sl-small) and [`t5-sl-large`](https://huggingface.co/cjvt/t5-sl-large) for paraphrasing. The models are available TODO *link*.

Should you so desire, you can fine tune the models yourself. Note that, if you have a GPU with <= 8GB of RAM, you need to use the small version of t5, i.e. `t5-sl-small`. In our case, the large model needs more than 8GB of RAM for successful training. In case the train script produces an OOM (OutOfMemory) error, try changing `batch_size` to something smaller.

If you have (access to) a more powerful machine, to use the large model you simply need to change model and tokenizer in [`train_model.py`](train_model.py) to be `t5-sl-large` instead of `t5-sl-small`.

TODO choose the tokenized dataset ... etc



## Testing the model

For testing, we provided a [`simple_test.py`](simple_test.py) script. This script will load a model of your choosing and generate a paraphase, based on input text and sampling method.

TODO add more ...
TODO more sections ...


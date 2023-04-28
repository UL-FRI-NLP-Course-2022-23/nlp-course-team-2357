# Natural language processing course 2022/23: Paraphrasing sentences <!-- omit in toc -->

Team members:
 * Mitja Vendramin, 63170301, mv2825@student.uni-lj.si
 * Luka Boljević, 63210482, lb7093@student.uni-lj.si
 * Matjaž Bizjak, 63170054, mb0539@student.uni-lj.si
 
Group public acronym/name: nlp-course-team-2357



# Table of contents <!-- omit in toc -->

- [Dataset](#dataset)
- [Docker](#docker)
- [Slovene NMT](#slovene-nmt)
- [Manual setup of Slovene NMT](#manual-setup-of-slovene-nmt)
  - [Prerequisites](#prerequisites)
  - [Setting it up](#setting-it-up)



# Dataset

The [ccKres dataset](https://www.clarin.si/repository/xmlui/handle/11356/1034) used for this project can be downloaded simply by running the `download_dataset.py` script. Read more about ccKres and open Slovene corpora in general on [this link](http://eng.slovenscina.eu/korpusi/proste-zbirke).

The dataset will be extracted inside the folder `cckres`, with the following structure:
- `cckres/text` contains files with raw, unprocessed text of the corpus.
- `cckres/xml` contains the corresponding `xml` files, which split the raw text into paragraphs, sentences, and words. The lemma and [Slovene MSD](http://nl.ijs.si/jos/josMSD-en.html) (Morpho-Syntactic Descriptor) of each word is known.
- `cckres/vert` contains a single file, `cckres.vert`, a vertical file containing *all* text from the corpus, split into paragraphs, sentences, and words, with lemmas, Slovene and English MSDs known for each word.


# Docker

To set up the translation service, Docker needs to be installed on your machine. If it is, you can freely skip this section. 

On Windows, the easiest way to install Docker is to download [Docker Desktop](https://docs.docker.com/desktop/install/windows-install/). Simply download the installer, and run it to install. 

Docker Desktop requires WSL (Windows Subsystem for Linux) version 2 to run properly. If you do not have WSL on your Windows machine, it can be installed by simply going opening PowerShell in **administrator** mode, and executing `wsl --install`, as specified [here](https://learn.microsoft.com/en-us/windows/wsl/install#install-wsl-command). You do not actually need to do anything else with WSL, you just need to have it installed.

---

On Linux, Docker can simply be installed by following the instructions on [this link](https://docs.docker.com/engine/install/ubuntu/). If you get a post installation error, fix it by running the command from [this answer](https://askubuntu.com/a/1302888) first, and then rerun the installation.

To avoid having to run docker as sudo all the time, follow the short instructions on [this link](https://docs.docker.com/engine/install/linux-postinstall/).



# Slovene NMT

To set up [Slovene_NMT](https://github.com/clarinsi/Slovene_NMT) (Neural Machine Translator), simply run one of the available scripts:
- `./setup_translator_linux.sh`, if you are using Linux,
- `./setup_translator_gitbash.sh`, if you are on Windows and prefer using [Git Bash](https://git-scm.com/downloads),
- `& .\setup_translator_powershell.ps1`, if you are on Windows and prefer using PowerShell. In this case, you need to run PowerShell as **Administrator** for the script to work. Please keep in mind that downloading the NVIDIA models via PowerShell is rather slow. If you want, you can manually download and place the NVIDIA models in the appropriate directory inside `Slovene_NMT`, and comment out unnecessary commands in the script.

All scripts accept arguments `cpu` and `gpu`. Run the script applicable to you, with the argument `cpu`, if you want to deploy on CPU, or `gpu` if you want to deploy on (NVIDIA) GPU. All scripts will do the following:
- Install the `zstd` program, required to decompress pretrained NVIDIA NeMo translation models, compressed as `.tar.zst` files.
- Pull the image `nvcr.io/nvidia/pytorch:22.08-py3` from Dockerhub. This is done prior to building the containers with docker compose, as there might be some authorization errors otherwise.
- Clone and prepare the `Slovene_NMT` repository
- Download the NeMo translation models from the very bottom of [this page](https://www.clarin.si/repository/xmlui/handle/11356/1736).
- After decompressing and unzipping the models, build and run the containers for translation.

Running the script for the first time takes a while, so simply let it run until completion. Also note that inside the scripts, there is a line intended for deleting the downloaded (`.tar.zst`) and extracted (`.tar`) NVIDIA model archives. Inside the two Windows scripts, there are two lines that remove the downloaded `zstd` program. All of those lines are currently commented, but feel free to uncomment them.

You may notice that the docker compose files the scripts will copy into `Slovene_NMT` split the translation service into two containers - one for English to Slovene, and one for Slovene to English translation. This is different to original docker compose files from `Slovene_NMT`, where the deployment places both translation services in one container, but we deemed this unnecessary.

Note that the API of the two containers will not be available until the model is loaded inside the container, which can take about 6 to 7 minutes. It is best to stream the logs with `docker logs -f translator_slen` i.e. `docker logs -f translator_ensl` and see exactly when the initialization finishes. After it finishes, the API will be available on `localhost` ports 4001 (English to Slovene translation) and 4002 (Slovene to English translation). Check the file [`SloveneNMT_example_usage.md`](SloveneNMT_example_usage.md) for details how to use the API.

**Important note**: on Windows, the two Docker containers that will be created, coupled with the VM Docker Desktop uses in the background, can in total easily take up 12-13GB of RAM just to be able to run. If you have more than 16GB of RAM, you should be okay, but if you don't, we **strongly** suggest running one container at a time.

Setting up `Slovene_NMT` can also be done "manually". The steps are included at the bottom of this README, in section [Manual setup of Slovene NMT](#manual-setup-of-slovene-nmt), for completeness sake.



---
---



# Manual setup of Slovene NMT

## Prerequisites

To make setting up Slovene NMT as painless as possible, we will first list what you are required to download and/or install, before getting into the actual set up.

- Open a terminal, and run the command:
    ```bash
    docker pull nvcr.io/nvidia/pytorch:22.08-py3
    ```
    This is done prior to building the containers with docker compose, as there might be some authorization errors otherwise.

- Slovene NMT needs pretrained NVIDIA NeMo models for the translation. The two models can be downloaded from the very bottom of [this page](https://www.clarin.si/repository/xmlui/handle/11356/1736).

- The two NMT models are compressed as `.tar.zst` files. You will need the `zstd` program to decompress them.
   - On Windows, download the latest release of `zstd` from [this link](https://github.com/facebook/zstd/releases), which at the time of writing is v1.5.5. In other words, `zstd-v1.5.5-win64.zip` needs to be downloaded. After downloading, extract the zip archive to the location of your choosing.
   - If you are on Linux, install `zstd` with `sudo apt-get install zstd -y`.


## Setting it up

After waiting for the NVIDIA Docker image to be pulled, downloading the two NeMo model files, and installing `zstd`, you are equipped to set up `Slovene_NMT`.

1. In the folder where this repository is cloned, clone the `Slovene_NMT` repository:
    ```bash
    git clone https://github.com/clarinsi/Slovene_NMT.git
    ```
    Move inside of folder `Slovene_NMT`.

2. Inside `Slovene_NMT`, create a folder called `models`. Move the two downloaded NeMo model files, namely `slen_GEN_nemo-1.2.6.tar.zst` and `ensl_GEN_nemo-1.2.6.tar.zst`, inside that folder.

3. Decompress the `.tar.zst` files using the `zstd` program you downloaded:
   - On Windows, run the following two commands (notice that you need to supply the relative path to `zstd.exe`):
    ```powershell
    path/to/zstd.exe -d slen_GEN_nemo-1.2.6.tar.zst
    ```
    ```powershell
    path/to/zstd.exe -d ensl_GEN_nemo-1.2.6.tar.zst
    ```
   - On Linux, run the following two commands:
    ```bash
    zstd -d slen_GEN_nemo-1.2.6.tar.zst
    ```
    ```bash
    zstd -d ensl_GEN_nemo-1.2.6.tar.zst
    ```
    
    Running the commands should result in two archives, `slen_GEN_nemo-1.2.6.tar` and `ensl_GEN_nemo-1.2.6.tar`.

4. Newly created `.tar` archives need to be unzipped.
    - On Linux, you can also right click on the archives, and click "Extract Here". If you prefer using the terminal, you can use the `tar -xf` command:
    ```bash
    tar -xf slen_GEN_nemo-1.2.6.tar
    ```
    ```bash
    tar -xf ensl_GEN_nemo-1.2.6.tar
    ```
    - On Windows, you can use WinRAR to unzip the archives. Right click on the archives, and click "Extract Here". You can also use the same `tar -xf` command, both in Git Bash *and* PowerShell.
    
    Unzipping the archives results in two new folders inside `models/v1.2.6`: `ensl` and `slen`. Each of these folders contains a `model.info` file and an `aayn_base.nemo` file, which together form the pretrained models for translating English to Slovene and Slovene to English, respectively.

5. You can now safely delete, or at the very least move the two `.tar.zst` and two `.tar` archives from `models`, as they are not needed anymore, but you don't have to.

6. In the root of `Slovene_NMT`, edit the existing `Dockerfile` to have the following contents:
    ```docker
    FROM nvcr.io/nvidia/pytorch:22.08-py3 as nemo

    ARG DEBIAN_FRONTEND=noninteractive

    RUN apt-get update \
        && apt-get upgrade -y \
        && git clone https://github.com/NVIDIA/NeMo.git /workspace/nemo \
        && cd /workspace/nemo \
        && git checkout v1.11.0 \
        && ./reinstall.sh

    FROM nemo as service

    ARG DEBIAN_FRONTEND=noninteractive

    COPY . /opt/nmt
    RUN python3 -m pip install -r /opt/nmt/requirements.txt
    WORKDIR /opt/nmt

    ENTRYPOINT [ "python3", "server.py" ]
    ```
    The difference between this `Dockerfile` and the original one is in one line - `&& python3 -m pip install --upgrade pip \`. We removed this line because deployment will fail if pip is upgraded.

7. In the root of `Slovene_NMT`, edit the existing `docker-compose.yml` file to have the following contents:
    ```yaml
    services:
      translator_ensl:
        restart: unless-stopped
        image: rsdo/ds4/nemo-nmt:latest
        build: .
        container_name: translator_ensl
        ports:
          - 4001:4000
        volumes:
          - type: bind
            source: ./models/v1.2.6/ensl
            target: /opt/nmt/models/v1.2.6
            read_only: true

      translator_slen:
        restart: unless-stopped
        image: rsdo/ds4/nemo-nmt:latest
        build: .
        container_name: translator_slen
        ports:
          - 4002:4000
        volumes:
          - type: bind
            source: ./models/v1.2.6/slen
            target: /opt/nmt/models/v1.2.6
            read_only: true
    ```
    When we run `docker compose up` later, this should create two containers - one for English to Slovene translation, and another for Slovene to English translation. Loading both models inside of one container is simply not necessary. Another reason for this was that GPU deployment, on our team's best GPU (RTX 3070 with 8GB VRAM), was actually impossible, due to very large memory requirements.
    
    If you are going to be deploying on an NVIDIA GPU, also edit the existing `docker-compose.gpu.yml` file to contain the following:
    ```yaml
    services:
      translator_ensl:
        deploy:
          resources:
            reservations:
              devices:
                - capabilities:
                  - gpu
      translator_slen:
        deploy:
          resources:
            reservations:
              devices:
                - capabilities:
                  - gpu
    ```

8. Finally, you can deploy the translator:
    -  To deploy on CPU, run
    ```bash
    docker compose up -d
    ```
    - To deploy on GPU, run
    ```bash
    docker compose -f docker-compose.yml -f docker-compose.gpu.yml up -d
    ```

    Deploying will take a bit of time, even having prepulled the required `nvcr.io/nvidia/pytorch:22.08-py3` image, so be patient.
    
9. After the two containers have been created and started, the models need to be loaded inside the container before the API is available. You can check the status by streaming the logs of the container via `docker logs -f translator_slen` and `docker logs -f translator_ensl`. If everything was set up correctly, the final few lines of the logs of eg. `translator_ensl` should be something similar to the following:
    ```console
    [NeMo I 2023-04-11 19:05:19 save_restore_connector:243] Model MTEncDecModel was successfully restored from /opt/nmt/models/v1.2.6/aayn_base.nemo.
    [NeMo I 2023-04-11 19:05:21 server:284] Loaded models [('ensl:GEN:nemo-1.2.6', 'gpu')]
    [NeMo I 2023-04-11 19:05:21 server:285] Initialization finished in 283.24s
    INFO:     Started server process [1]
    INFO:     Waiting for application startup.
    INFO:     Application startup complete.
    INFO:     Uvicorn running on http://0.0.0.0:4000 (Press CTRL+C to quit)
    ```
# Model training
As our base model we chose [cjvt](https://huggingface.co/cjvt). We have two option. Either large or small t5 model. If you have a GPU with 8GB of RAM, you need to use the small version of the model. It is not documented on the model readme, but in our case the large model needs more than 8GB of RAM for succesfull training. If you want to use the large model you simply need to change model and tokenizer from small to large. In case, you have less than 8GB of GPU memory and the script produces OOM error, you can change the batch_size to a smaller number. You don't need to download anything. The script will automaticly download the model and tokenizer. After the script has finished, the new model will be saved in folder /Paraphrase_generator.

## Testing the new model
For quick debuging, and testing if the model even generates anything, we provided a simple_test.py script. This script will load the new model and generate a response.

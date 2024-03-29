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

After waiting for the NVIDIA Docker image to be pulled, downloading the two NeMo model files, and installing `zstd`, you can now set up `Slovene_NMT`.

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

5. You can now safely delete the two `.tar.zst` and two `.tar` archives from `models`, as they are not needed anymore, but you don't have to. You can leave them where they are.

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
    
    If you are going to be deploying on a GPU, also edit the existing `docker-compose.gpu.yml` file to contain the following:
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

    Deploying will take a bit of time, even having prepulled the required `nvcr.io/nvidia/pytorch:22.08-py3` image, so be patient. Note that GPU deployment is possible only on NVIDIA GPUs.
    
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

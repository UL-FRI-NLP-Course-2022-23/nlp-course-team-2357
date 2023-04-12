# Natural language processing course 2022/23: Paraphrasing sentences

Team members:
 * Mitja Vendramin, 63170301, mv2825@student.uni-lj.si
 * Luka Boljević, 63210482, lb7093@student.uni-lj.si
 * Matjaž Bizjak, 63170054, mb0539@student.uni-lj.si
 
Group public acronym/name: nlp-course-team-2357



# Docker

Make sure that before you start anything, Docker is installed on your machine. If it is, you can freely skip this section. We also suggest a 16GB RAM machine, as the Docker containers we will create later can take up as much as ~12GB of RAM at peak memory usage.
 
On Windows, the easiest way to install Docker is to download [Docker Desktop](https://docs.docker.com/desktop/install/windows-install/). Simply download the installer, and run it to install. 

Docker Desktop requires WSL (Windows Subsystem for Linux) version 2 to run properly. If you do not have WSL on your Windows machine, it can be installed by simply going opening PowerShell in **administrator** mode, and executing `wsl --install`, as specified [here](https://learn.microsoft.com/en-us/windows/wsl/install#install-wsl-command). You do not actually need to do anything else with WSL, you just need to have it installed.

---

On Linux, Docker can simply be installed by following the instructions on [this link](https://docs.docker.com/engine/install/ubuntu/). If you get a post installation error, fix it by running the command from [this answer](https://askubuntu.com/a/1302888) first, and then rerun the installation.

To avoid having to run docker as sudo all the time, follow the short instructions on [this link](https://docs.docker.com/engine/install/linux-postinstall/).



# Slovene NMT

To set up [Slovene NMT](https://github.com/clarinsi/Slovene_NMT) (Neural Machine Translator), simply run the script `./setup_translator.sh` with the argument `cpu`, if you want to deploy on CPU, or `gpu` if you want to deploy on (NVIDIA) GPU. The script will do the following:
- Install the `zstd` program, required to decompress pretrained NVIDIA NeMo translation models, compressed as `.tar.zst` files.
- Pull the image `nvcr.io/nvidia/pytorch:22.08-py3` from Dockerhub. This is done prior to building the containers with docker compose, as there might be some authorization errors otherwise.
- Download the NeMo translation models from the very bottom of [this page](https://www.clarin.si/repository/xmlui/handle/11356/1736).
- After decompressing and unzipping the models, build and run the containers for translation.

Running the script for the first time takes a while, so simply let it run until completion. Notice that currently, the script can only be run on Linux. A Windows script will be added in the future. 

For now, setting up Slovene NMT on Windows needs to be done "manually". To make it as painless as possible, we will first list what you are required to download and/or install, before getting into the actual set up. You can perform the same steps on Linux of course.


## Prerequisites

We will now list what you need to download and/or install, before getting into the actual set up of Slovene NMT.

- Open a terminal, and run the command:
    ```bash
    docker pull nvcr.io/nvidia/pytorch:22.08-py3
    ```
    This is done prior to building the containers with docker compose, as there might be some authorization errors otherwise.

- Slovene NMT needs pretrained NVIDIA NeMo models for the translation. The two models can be downloaded from the very bottom of [this page](https://www.clarin.si/repository/xmlui/handle/11356/1736).

- The two NMT models are compressed as `.tar.zst` files. You will need the `zstd` program to decompress them.
   - On Windows, download the latest release of `zstd` from [this link](https://github.com/facebook/zstd/releases), which at the time of writing is v1.5.5. In other words, `zstd-v1.5.5-win64.zip` needs to be downloaded. After downloading, extract the zip file to wherever you want.
   - If you are on Linux, install `zstd` with `sudo apt-get install zstd -y`.


## Setting up Slovene NMT

After waiting for the NVIDIA Docker image to be pulled, downloading the two NeMo model files, and installing `zstd`, you are equipped to set up Slovene NMT.

1. In the folder where this repository is cloned, clone the Slovene NMT repository:
    ```bash
    git clone https://github.com/clarinsi/Slovene_NMT.git
    ```
    Move inside of folder `Slovene_NMT`.

2. Inside Slovene_NMT, create a folder called `models`. Move the two downloaded NeMo model files, namely `slen_GEN_nemo-1.2.6.tar.zst` and `ensl_GEN_nemo-1.2.6.tar.zst`, inside that folder.

3. Decompress the `.tar.zst` files using the `zstd` program you downloaded:
   - On Windows, run the following two commands:
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
    - On Windows, you can use WinRAR to unzip the archives. Right click on the archives, and click "Extract Here".
    - On Linux, you can also right click on the archives, and click "Extract Here". If you prefer using the terminal, you can use the `tar -xf` command:
    ```bash
    tar -xf slen_GEN_nemo-1.2.6.tar
    ```
    ```bash
    tar -xf ensl_GEN_nemo-1.2.6.tar
    ```
    
    Unzipping the archives results in two new folders inside `models/v1.2.6`: `ensl` and `slen`. Each of these folders contains a `model.info` file and an `aayn_base.nemo` file, which together form the pretrained models for translating English to Slovene and Slovene to English, respectively.

5. You can now safely delete, or at the very least move the two `.tar.zst` and two `.tar` archives from `models`, as they are not needed anymore.

6. In the root of `Slovene_NMT`, edit the existing `docker-compose.yml` file to have the following contents:
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
    When we run `docker compose up` later, this should create two containers - one for English to Slovene translation, and another for Slovene to English translation. Loading both models inside of one container is not necessary, and actually not even possible on a system with an 8GB GPU, due to very large memory requirements.
    
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

7. Finally, you can deploy the translator:
    -  To deploy on CPU, run
    ```bash
    docker compose up -d
    ```
    - To deploy on GPU, run
    ```bash
    docker compose -f docker-compose.yml -f docker-compose.gpu.yml up -d
    ```

    Deploying will take a bit of time, even having prepulled the required `nvcr.io/nvidia/pytorch:22.08-py3` image, so be patient.
    
8. After the two containers have been created and started, the models need to be loaded inside the container before the API is available. You can check the status by streaming the logs of the container via `docker logs -f translator_slen` and `docker logs -f translator_ensl`. If everything was set up correctly, the final few lines of the logs of eg. `translator_ensl` should be something similar to the following:
    ```console
    [NeMo I 2023-04-11 19:05:19 save_restore_connector:243] Model MTEncDecModel was successfully restored from /opt/nmt/models/v1.2.6/aayn_base.nemo.
    [NeMo I 2023-04-11 19:05:21 server:284] Loaded models [('ensl:GEN:nemo-1.2.6', 'gpu')]
    [NeMo I 2023-04-11 19:05:21 server:285] Initialization finished in 283.24s
    INFO:     Started server process [1]
    INFO:     Waiting for application startup.
    INFO:     Application startup complete.
    INFO:     Uvicorn running on http://0.0.0.0:4000 (Press CTRL+C to quit)
    ```


## Example usage

The translation service can now be accessed via `localhost`. Based on the new docker compose file we used, English to Slovene translation will be available on port 4001, while Slovene to English translation will be available on port 4002.

### Health Check

To do a health check of the English to Slovene container, you can:
- Go to `localhost:4001/api/healthCheck`, or
- From the terminal (we recommend Git Bash on Windows), run `curl -X GET localhost:4001/api/healthCheck`. 
    
The output should be something like:
```json
{
    "status": 0,
    "start_time": "2023-04-11T19:05:27.927677+00:00",
    "models": [
        {
            "tag": "ensl:GEN:nemo-1.2.6",
            "workers": {
                "platform": "gpu",
                "active": 0
            },
            "features": null,
            "info": null
        }
    ],
    "num_requests_processed": 0
}
```

To do the same for Slovene to English container, just replace port 4001 with port 4002.

### Translation

To perform English to Slovene translation, create the following example `ensl.json` file:
```json
{
    "src_language": "en",
    "tgt_language": "sl",
    "text": "Today was a sunny day. Hopefully, it will be sunny tomorrow as well."
}
```

Then, from the terminal (we recommend Git Bash on Windows), run:
```bash
curl -X POST -H "Content-Type: application/json" -d @ensl.json http://localhost:4001/api/translate
```

Translation should take a few seconds, and the result should be:
```json
{
    "result": "Danes je bil sončen dan in upam, da bo tudi jutri sončno."
}
```

---

To do Slovene to English translation, create the following example `slen.json` file:
```json
{
    "src_language": "sl",
    "tgt_language": "en",
    "text": "Danes prijetno sneži. Jutri bo pa še lepše."
}
```

Then, from the terminal, run:
```bash
curl -X POST -H "Content-Type: application/json" -d @slen.json http://localhost:4002/api/translate
```

The returned result should be:
```json
{
    "result": "It snows well today, and tomorrow it will be even better."
}
```

### Stopping the containers

When you are done with translations, stop the containers with `docker stop translator_ensl` and `docker stop translator_slen`.

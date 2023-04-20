#!/bin/bash

if [ "$1" != "gpu" ] || [ "$1" != "cpu" ];
then
    echo "Please specify either 'gpu' (to deploy on GPU) or 'cpu' (to deploy on CPU) as the first argument."
    exit
fi

# Download zstd and extract
curl https://github.com/facebook/zstd/releases/download/v1.5.5/zstd-v1.5.5-win64.zip -L -o zstd.zip
unzip -q -o zstd.zip

# Image necessary for Slovene NMT
docker pull nvcr.io/nvidia/pytorch:22.08-py3

if [ ! -d "Slovene_NMT" ];
then
    git clone https://github.com/clarinsi/Slovene_NMT.git
fi

cp docker-compose.gpu.yml Slovene_NMT/docker-compose.gpu.yml
cp docker-compose.yml Slovene_NMT/docker-compose.yml

cd Slovene_NMT
mkdir models -p
cd models

# NVIDIA models
if [ ! -f "slen_GEN_nemo-1.2.6.tar.zst" ];
then
    curl --remote-name https://www.clarin.si/repository/xmlui/bitstream/handle/11356/1736/slen_GEN_nemo-1.2.6.tar.zst
fi
if [ ! -f "ensl_GEN_nemo-1.2.6.tar.zst" ];
then
    curl --remote-name https://www.clarin.si/repository/xmlui/bitstream/handle/11356/1736/ensl_GEN_nemo-1.2.6.tar.zst
fi

# Extract all archives
../../zstd-v1.5.5-win64/zstd.exe -d slen_GEN_nemo-1.2.6.tar.zst -f
../../zstd-v1.5.5-win64/zstd.exe -d ensl_GEN_nemo-1.2.6.tar.zst -f 
tar -xf slen_GEN_nemo-1.2.6.tar
tar -xf ensl_GEN_nemo-1.2.6.tar

# Feel free to uncomment these lines if you want to remove the archives and zstd
# rm *.zst *.tar
# rm -R ../../zstd
# rm ../../zstd.zip

# Deploy
cd ..
if [ "$1" = "gpu" ];
then
    docker compose -f docker-compose.yml -f docker-compose.gpu.yml up -d
elif [ "$1" = "cpu" ];
then
    docker compose up -d
fi

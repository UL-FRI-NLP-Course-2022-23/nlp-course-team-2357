#!/bin/bash

if [ "$1" != "gpu" ] && [ "$1" != "cpu" ];
then
    echo "Please specify either 'gpu' (to deploy on GPU) or 'cpu' (to deploy on CPU) as the first argument."
    exit
fi

cd ..

# Download zstd and extract. Zstd is necessary to extract .tar.zst archives.
curl https://github.com/facebook/zstd/releases/download/v1.5.5/zstd-v1.5.5-win64.zip -L -o zstd.zip
unzip -q -o zstd.zip -d zstd

# Image necessary for Slovene NMT
docker pull nvcr.io/nvidia/pytorch:22.08-py3

# Clone repository
if [ ! -d "Slovene_NMT" ];
then
    git clone https://github.com/clarinsi/Slovene_NMT.git
fi

# Modify Docker related files so deployment can work (or work better)
cp nmt_files/docker-compose.gpu.yml Slovene_NMT/docker-compose.gpu.yml
cp nmt_files/docker-compose.yml Slovene_NMT/docker-compose.yml
cp nmt_files/Dockerfile Slovene_NMT/Dockerfile

cd Slovene_NMT
mkdir models -p
cd models

# Download NVIDIA models
if [ ! -f "slen_GEN_nemo-1.2.6.tar.zst" ];
then
    curl --remote-name https://www.clarin.si/repository/xmlui/bitstream/handle/11356/1736/slen_GEN_nemo-1.2.6.tar.zst
fi
if [ ! -f "ensl_GEN_nemo-1.2.6.tar.zst" ];
then
    curl --remote-name https://www.clarin.si/repository/xmlui/bitstream/handle/11356/1736/ensl_GEN_nemo-1.2.6.tar.zst
fi

# Extract all archives
echo "Extracting slen_GEN_nemo-1.2.6.tar.zst ..."
../../zstd/zstd-v1.5.5-win64/zstd.exe -d slen_GEN_nemo-1.2.6.tar.zst -f 
echo "Extracting ensl_GEN_nemo-1.2.6.tar.zst ..."
../../zstd/zstd-v1.5.5-win64/zstd.exe -d ensl_GEN_nemo-1.2.6.tar.zst -f
echo "Extracting slen_GEN_nemo-1.2.6.tar ..."
tar -xf slen_GEN_nemo-1.2.6.tar
echo "Extracting ensl_GEN_nemo-1.2.6.tar ..."
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
fi
if [ "$1" = "cpu" ];
then
    docker compose up -d
fi

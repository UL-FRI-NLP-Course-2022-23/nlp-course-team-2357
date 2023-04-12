#!/bin/bash

#docker run -it --rm nvcr.io/nvidia/pytorch:22.08-py3 bash

if [ ! -d = "Slovene_NMT" ];
then
    docker pull nvcr.io/nvidia/pytorch:22.08-py3

    git clone https://github.com/clarinsi/Slovene_NMT.git

    cp docker-compose.gpu.yml Slovene_NMT/docker-compose.gpu.yml
    cp docker-compose.yml Slovene_NMT/docker-compose.yml

    cd Slovene_NMT

    curl --remote-name-all https://www.clarin.si/repository/xmlui/bitstream/handle/11356/1736{/slen_GEN_nemo-1.2.6.tar.zst,/ensl_GEN_nemo-1.2.6.tar.zst}

    zstd -d slen_GEN_nemo-1.2.6.tar.zst
    zstd -d ensl_GEN_nemo-1.2.6.tar.zst

    tar -xf slen_GEN_nemo-1.2.6.tar
    tar -xf ensl_GEN_nemo-1.2.6.tar

    rm *.zst *.tar

    if [ "$1" = "gpu" ];
    then
        docker compose -f docker-compose.yml -f docker-compose.gpu.yml up -d
    fi
    if [ "$1" = "cpu" ];
    then
        docker compose up -d
    fi
fi

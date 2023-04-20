if ($args[0] -ne "gpu" -or $args[0] -ne "cpu"){
    Write-Host "Please specify either 'gpu' (to deploy on GPU) or 'cpu' (to deploy on CPU) as the first argument."
    exit
}

# Download zstd and extract
Invoke-WebRequest -Uri https://github.com/facebook/zstd/releases/download/v1.5.5/zstd-v1.5.5-win64.zip -OutFile zstd.zip
Expand-Archive zstd.zip -Force

# Image necessary for Slovene NMT
docker pull nvcr.io/nvidia/pytorch:22.08-py3

if (-not (Test-Path "Slovene_NMT")){
    git clone https://github.com/clarinsi/Slovene_NMT.git
}

Copy-Item -Path docker-compose.gpu.yml -Destination Slovene_NMT/docker-compose.gpu.yml
Copy-Item -Path docker-compose.yml -Destination Slovene_NMT/docker-compose.yml

Set-Location Slovene_NMT
if (-not (Test-Path "models")){
    mkdir models
}
Set-Location models

# NVIDIA models
# $TLS12Protocol = [System.Net.SecurityProtocolType] 'Ssl3 , Tls12'
# [System.Net.ServicePointManager]::SecurityProtocol = $TLS12Protocol
if (-not (Test-Path "slen.tar.zst")){
    Invoke-WebRequest -Uri https://www.clarin.si/repository/xmlui/bitstream/handle/11356/1736/slen_GEN_nemo-1.2.6.tar.zst -OutFile slen.tar.zst -Verbose
}
if (-not (Test-Path "ensl.tar.zst")){
    Invoke-WebRequest -Uri https://www.clarin.si/repository/xmlui/bitstream/handle/11356/1736/ensl_GEN_nemo-1.2.6.tar.zst -OutFile ensl.tar.zst -Verbose
}

# Extract all archives
../../zstd/zstd-v1.5.5-win64/zstd.exe -d slen.tar.zst -f
../../zstd/zstd-v1.5.5-win64/zstd.exe -d ensl.tar.zst -f
tar -xf slen.tar
tar -xf ensl.tar

# Feel free to uncomment these lines if you want to remove the archives and zstd
# Remove-Item *.zst *.tar
# Remove-Item -Recurse ../../zstd
# Remove-Item ../../zstd.zip

# Deploy
Set-Location ..
if ($args[0] -eq "gpu"){
    docker compose -f docker-compose.yml -f docker-compose.gpu.yml up -d
}
elseif ($args[0] -eq "cpu"){
    docker compose up -d
}

Set-Location ..

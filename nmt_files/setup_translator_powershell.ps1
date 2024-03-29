if ($args[0] -ne "gpu" -and $args[0] -ne "cpu"){
    Write-Host "Please specify either 'gpu' (to deploy on GPU) or 'cpu' (to deploy on CPU) as the first argument."
    exit
}

Set-Location ..

# Download zstd and extract. Zstd is necessary to extract .tar.zst archives.
Invoke-WebRequest -Uri https://github.com/facebook/zstd/releases/download/v1.5.5/zstd-v1.5.5-win64.zip -OutFile zstd.zip
Expand-Archive zstd.zip -Force

# Image necessary for Slovene NMT
docker pull nvcr.io/nvidia/pytorch:22.08-py3

# Clone repository
if (-not (Test-Path "Slovene_NMT")){
    git clone https://github.com/clarinsi/Slovene_NMT.git
}

# Modify Docker related files so deployment can work (or work better)
Copy-Item -Path nmt_files/docker-compose.gpu.yml -Destination Slovene_NMT/docker-compose.gpu.yml
Copy-Item -Path nmt_files/docker-compose.yml -Destination Slovene_NMT/docker-compose.yml
Copy-Item -Path nmt_files/Dockerfile -Destination Slovene_NMT/Dockerfile

Set-Location Slovene_NMT
if (-not (Test-Path "models")){
    mkdir models
}
Set-Location models

# Download NVIDIA models. Note that downloading via PowerShell is quite slow.
# Before running this script, you can manually download the archives, and place them in Slovene_NMT/models.
if (-not (Test-Path "slen_GEN_nemo-1.2.6.tar.zst")){
    Invoke-WebRequest -Uri https://www.clarin.si/repository/xmlui/bitstream/handle/11356/1736/slen_GEN_nemo-1.2.6.tar.zst -OutFile slen_GEN_nemo-1.2.6.tar.zst
}
if (-not (Test-Path "ensl_GEN_nemo-1.2.6.tar.zst")){
    Invoke-WebRequest -Uri https://www.clarin.si/repository/xmlui/bitstream/handle/11356/1736/ensl_GEN_nemo-1.2.6.tar.zst -OutFile ensl_GEN_nemo-1.2.6.tar.zst
}

# Extract all archives
Write-Host "Extracting slen_GEN_nemo-1.2.6.tar.zst ..."
../../zstd/zstd-v1.5.5-win64/zstd.exe -d slen_GEN_nemo-1.2.6.tar.zst -f
Write-Host "Extracting ensl_GEN_nemo-1.2.6.tar.zst ..."
../../zstd/zstd-v1.5.5-win64/zstd.exe -d ensl_GEN_nemo-1.2.6.tar.zst -f
Write-Host "Extracting slen_GEN_nemo-1.2.6.tar ..."
tar -xf slen_GEN_nemo-1.2.6.tar
Write-Host "Extracting ensl_GEN_nemo-1.2.6.tar ..."
tar -xf ensl_GEN_nemo-1.2.6.tar

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

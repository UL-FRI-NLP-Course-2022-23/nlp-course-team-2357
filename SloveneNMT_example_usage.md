# Slovene_NMT example usage

After setting up Slovene NMT and waiting for the models to load inside the container(s), the translation services can be accessed via `localhost`. English to Slovene translation API will be available on port 4001, while Slovene to English translation API will be available on port 4002. 


## Health Check

To do a health check of the English to Slovene container, you can:
1. Go to `localhost:4001/api/healthCheck` in your browser, or
2. Use the terminal:
    - On Linux, run:
    ```bash
    curl -X GET http://localhost:4001/api/healthCheck | python3 -m json.tool
    ```
    - In Git Bash, run:
    ```bash
    curl -X GET http://localhost:4001/api/healthCheck | python.exe -m json.tool
    ```
    - In PowerShell, run:
    ```powershell
    Invoke-RestMethod -Method Get -Uri http://localhost:4001/api/healthCheck | ConvertTo-Json
    ```
    
The result should be something like:
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


## English to Slovene translation

To perform English to Slovene translation, create the following example `ensl.json` file:
```json
{
    "src_language": "en",
    "tgt_language": "sl",
    "text": "Today was a sunny day. Hopefully, it will be sunny tomorrow as well."
}
```

Then, from the terminal:
- On Linux and Git Bash on Windows, run:
    ```bash
    curl -X POST -H "Content-Type: application/json" -d @ensl.json http://localhost:4001/api/translate
    ```
- In PowerShell, run:
    ```powershell
    Invoke-RestMethod -Method Post -Uri "http://localhost:4001/api/translate" -ContentType "application/json" -Body (Get-Content ensl.json -Encoding UTF8)
    ```

Translation should take a few seconds, and the result should be:
```json
{
    "result": "Danes je bil sončen dan in upam, da bo tudi jutri sončno."
}
```


## Slovene to English translation

To do Slovene to English translation, create the following example `slen.json` file:
```json
{
    "src_language": "sl",
    "tgt_language": "en",
    "text": "Danes prijetno sneži. Jutri bo pa še lepše."
}
```

Then, from the terminal:
- On Linux and Git Bash on Windows, run:
    ```bash
    curl -X POST -H "Content-Type: application/json" -d @slen.json http://localhost:4002/api/translate
    ```
- In PowerShell, run:
    ```powershell
    Invoke-RestMethod -Method Post -Uri "http://localhost:4002/api/translate" -ContentType "application/json; charset=utf-8" -Body (Get-Content slen.json -Encoding UTF8)
    ```


The returned result should be:
```json
{
    "result": "It snows well today, and tomorrow it will be even better."
}
```


## Stopping the containers

When you are done with translations, you can stop the containers with `docker stop translator_ensl` and `docker stop translator_slen`.
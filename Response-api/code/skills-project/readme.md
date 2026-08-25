## Linux
```sh
cd rca-skill
zip -r ../rca-skill-contents.zip .
```
## windows
```pwsh
Compress-Archive -Path .\rca-skill\* -DestinationPath .\rca-skill-contents.zip
``` 

## In Azure Cloud Shell
```sh
export MY_FOUNDRY_ENDPOINT="https://project-01-us.services.ai.azure.com/api/projects/14juneproject"
echo $MY_FOUNDRY_ENDPOINT
nano 1.py
python -m venv venv 
source venv/bin/activate
pip install azure-ai-projects azure-identity
python 1.py 
```


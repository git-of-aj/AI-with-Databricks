import json
import requests
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv()

credential = DefaultAzureCredential()

token = credential.get_token(
    "https://api.loganalytics.io/.default"
)

# print(token)

url = "https://api.loganalytics.io/v1/subscriptions/38e274f8-10b9-4348-bd1d-62d18e5458d1/resourceGroups/adf/providers/Microsoft.DataFactory/factories/adf-98/query?query=ADFActivityRun%0A%7C%20where%20Status%20has%20%22Failed%22%0A%7C%20project%20TimeGenerated%2C%20ResourceId%2C%20OperationName%2C%20ActivityName%2C%20ActivityType%2C%20PipelineName%2C%20Output%2C%20ErrorMessage%2C%20Error&timespan=2026-08-30T13%3a23%3a39.0000000Z%2f2026-08-30T13%3a28%3a39.0000000Z"

# response = requests.get(
#     url,
#     headers={
#         "Authorization": f"Bearer {token.token}"
#     },
#     timeout=60,
# )

response = requests.get(
    url,
    headers={
        "Authorization": f"Bearer {token.token}",
        "Prefer": "include-permissions=true",
    },
    timeout=60,
)


print("Status:", response.status_code)
print("Headers:", dict(response.headers))

try:
    print(json.dumps(response.json(), indent=2))
except Exception:
    print(response.text)

response.raise_for_status()

print(json.dumps(response.json(), indent=2))

# Run app:
```sh
mkdir code && cd code
curl -LsSf https://astral.sh/uv/install.sh | sh
uv python install 3.14
uv venv
source .venv/bin/activate
python --version
uv pip install agent-framework azure-identity dotenv
git clone https://github.com/git-of-aj/AI-with-Databricks.git
cd AI-with-Databricks/AI-Agents/Hosting_Agents
uv pip install -r requirements.txt 
uvicorn main:app --reload
```

#### GET /health
```sh
curl -X GET http://localhost:8000/health
```
#### POST /conversations
```sh
curl -X POST http://localhost:8000/conversations \
  -H "Content-Type: application/json" \
  -d '{}'
```
#### POST /chat
```sh
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello"
  }'
```
#### GET /
```sh
curl -X GET http://localhost:8000/
```

```sh
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "what was my first question",
    "conversation_id": "conv_83af56a8f083fdb3..."
  }'
```

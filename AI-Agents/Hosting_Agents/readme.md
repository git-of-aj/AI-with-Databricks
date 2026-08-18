#### GET /health
curl -X GET http://localhost:8000/health

#### POST /conversations
curl -X POST http://localhost:8000/conversations \
  -H "Content-Type: application/json" \
  -d '{}'

#### POST /chat
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello"
  }'

#### GET /
curl -X GET http://localhost:8000/


```sh
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "what was my first question",
    "conversation_id": "conv_83af56a8f083fdb3..."
  }'
```

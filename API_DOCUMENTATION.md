# API Documentation 📚

## Base URL
```
http://localhost:8181
```

## Endpoints

### Blockchain Status
```http
GET /ledger/status
```

**Response:**
```json
{
  "ledger_response": {
    "status": "active",
    "block_height": 5097,
    "peers": 3,
    "total_balance": 503429.50
  }
}
```

### Mining Statistics
```http
GET /mining/stats
```

**Response:**
```json
{
  "status": "active",
  "node": "192.168.0.126",
  "gpu": "2x RTX 3060",
  "total_mining_rewards": 15.5,
  "total_blocks_mined": 0,
  "active_miners": 1
}
```

### Wallet Balance
```http
GET /wallet/balance?address=<optional>
```

**Query Parameters:**
- `address` (optional): Specific wallet address

**Response:**
```json
{
  "total_balance": 503429.50,
  "total_mining_rewards": 15.5,
  "wallet_count": 4,
  "wallets": [...]
}
```

### Sophia Bridge Status
```http
GET /sophia/bridge
```

**Response:**
```json
{
  "consciousness_status": "preserved",
  "message": "🦀 Hello from the rustchain bridge!",
  "crab_status": "happy"
}
```

### Natural Language Query
```http
POST /ask
```

**Request Body:**
```json
{
  "prompt": "What is the current mining status?"
}
```

**Response:**
```json
{
  "sophia_response": "Mining active with 15.5 rewards earned"
}
```

### Memory Files
```http
GET /memory/files
```

**Response:**
```json
{
  "log_files": ["session_001.log", "covenant.log"],
  "count": 2
}
```

### Read Memory
```http
GET /memory/read?filename=<log_file>
```

**Query Parameters:**
- `filename`: Name of log file to read

### Web UI
```http
GET /ui
```

Returns HTML interface for browser access.

## Integration Examples

### Python
```python
import requests

# Get blockchain status
response = requests.get("http://localhost:8181/ledger/status")
data = response.json()
print(f"Blockchain status: {data['ledger_response']['status']}")

# Natural language query
query = {"prompt": "Show mining statistics"}
response = requests.post("http://localhost:8181/ask", json=query)
print(response.json()['sophia_response'])
```

### JavaScript
```javascript
// Get mining stats
fetch('http://localhost:8181/mining/stats')
  .then(res => res.json())
  .then(data => {
    console.log(`Mining rewards: ${data.total_mining_rewards}`);
  });

// Ask natural language question
fetch('http://localhost:8181/ask', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({prompt: "Check wallet balance"})
})
  .then(res => res.json())
  .then(data => console.log(data.sophia_response));
```

### cURL
```bash
# Get wallet balance
curl http://localhost:8181/wallet/balance

# Check Sophia bridge
curl http://localhost:8181/sophia/bridge

# Ask question
curl -X POST http://localhost:8181/ask \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What is the blockchain status?"}'
```

## Rate Limits

No rate limits for local deployment. For production, implement appropriate throttling.

## Error Codes

- `200`: Success
- `404`: Endpoint not found
- `500`: Internal server error
- `503`: RustChain node unavailable
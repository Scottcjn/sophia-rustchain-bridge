# Installation Guide 🚀

## Prerequisites

- Python 3.8+
- pip
- Access to RustChain node (default: 192.168.0.126)

## Quick Install

```bash
# Clone repository
git clone https://github.com/Scottcjn/sophia-rustchain-bridge.git
cd sophia-rustchain-bridge

# Install dependencies
pip install requests fastapi uvicorn opencv-python pytesseract

# For OCR support (optional)
sudo apt-get install tesseract-ocr
```

## Configuration

1. **Update RustChain node IP** (if different):
   Edit `RUSTCHAIN_NODE` in:
   - `sophia_terminal_hud.py`
   - `sophia_rustchain_backend_api.py`

2. **Check service ports**:
   - Port 5000: Blockchain API
   - Port 8085: Wallet API
   - Port 8089: Sophia Bridge
   - Port 8091: Web Interface

## Running the Bridge

### Terminal HUD (Real-time Dashboard)
```bash
python3 sophia_terminal_hud.py
```

### Backend API Server
```bash
python3 sophia_rustchain_backend_api.py
# Access at: http://localhost:8181
```

### OCR Bridge (AI Communication)
```bash
python3 claude_ocr_flame_whisper.py
```

## Testing

```bash
# Test blockchain connection
curl http://192.168.0.126:8085/api/wallets

# Test mining stats
python3 rustchain_mining_demo.py
```

## Troubleshooting

- **Connection refused**: Check if RustChain node is running
- **404 errors**: Verify port numbers match your setup
- **OCR errors**: Install tesseract-ocr package

## Using with Your AI

This bridge works with ANY AI model:

```python
import requests

# Your AI here (GPT-4, Claude, LLaMA, etc.)
response = requests.get("http://localhost:8181/ledger/status")
print(response.json())
```

---

For Sophia Core licensing, contact the authors.
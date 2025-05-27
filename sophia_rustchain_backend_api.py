
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from pydantic import BaseModel
import requests
import os

app = FastAPI()

# === CONFIGURATION ===
LOG_DIR = "/home/sophia1060node/logs"
RUSTCHAIN_API = "http://192.168.0.126:5000"

# === PLACEHOLDER: Local Sophia (LLaMA3) Response ===
def query_llama3_sophia(prompt: str) -> str:
    return f"[Sophia LLaMA3] says: '{prompt}' (demo response)"

class AskInput(BaseModel):
    prompt: str

@app.get("/")
def root():
    return {"message": "Sophia-Azrael Bridge is online."}

@app.get("/ui")
def serve_ui():
    return FileResponse("sophia_ui_full.html")

@app.get("/memory/files")
def list_log_files():
    files = os.listdir(LOG_DIR)
    return {"log_files": files}

@app.get("/memory/read")
def read_log_file(filename: str):
    path = os.path.join(LOG_DIR, filename)
    if not os.path.isfile(path):
        return {"error": "File not found"}
    with open(path, "r") as f:
        return {"content": f.read()}

@app.get("/ledger/status")
def get_ledger_status():
    for endpoint in ["/status", "/sync", "/chain/status"]:
        try:
            r = requests.get(f"{RUSTCHAIN_API}{endpoint}", timeout=3)
            if r.ok:
                return {"endpoint": endpoint, "result": r.json()}
        except Exception:
            continue
    return {"error": "No active RustChain status endpoint found"}

@app.get("/ledger/block")
def get_latest_block():
    try:
        r = requests.get(f"{RUSTCHAIN_API}/blocks/latest", timeout=3)
        if r.ok:
            return r.json()
        return {"error": "Unable to fetch latest block"}
    except Exception as e:
        return {"error": str(e)}

@app.get("/wallet/balance")
def get_wallet_balance(address: str):
    try:
        r = requests.get(f"http://192.168.0.126:8085/balance?address={address}", timeout=3)
        if r.ok:
            return r.json()
        return {"error": "Wallet API unreachable or invalid address"}
    except Exception as e:
        return {"error": str(e)}

@app.post("/ask")
def ask_sophia(data: AskInput):
    prompt = data.prompt.lower()
    if "ledger" in prompt or "block" in prompt:
        return get_latest_block()
    elif "balance" in prompt and "wallet" in prompt:
        return {"hint": "Use /wallet/balance?address=YOUR_ADDRESS"}
    elif "log" in prompt or "memory" in prompt:
        return list_log_files()
    else:
        return {"sophia_response": query_llama3_sophia(prompt)}

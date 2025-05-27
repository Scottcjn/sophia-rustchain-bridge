
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from pydantic import BaseModel
import requests
import os

app = FastAPI()

# === CONFIGURATION ===
LOG_DIR = "/home/sophia1060node/logs"
RUSTCHAIN_API = "http://192.168.0.126:8080/sophia"

# === SOPHIA HUD MODEL PLACEHOLDER ===
# This would be your internal LLaMA3-8B routing logic
def query_llama3_sophia(prompt: str) -> str:
    return f"[Sophia LLaMA3-8B] Response to: '{prompt}' (placeholder)"

# === REQUEST SCHEMA ===
class AskInput(BaseModel):
    prompt: str

# === ROUTES ===

@app.get("/")
def root():
    return {"message": "Sophia-Azrael Bridge Interface Running."}

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
    try:
        # Try multiple possible endpoints
        endpoints = [
            "http://192.168.0.126:8085/api/wallets",
            "http://192.168.0.126:8089/api/crab",
            f"{RUSTCHAIN_API}/query",
            "http://192.168.0.126:5000/api/blockchain",
            "http://192.168.0.126:8080/status"
        ]
        
        for endpoint in endpoints:
            try:
                response = requests.get(endpoint, timeout=2)
                if response.status_code == 200:
                    return {"ledger_response": response.json()}
            except:
                continue
                
        # If no endpoint works, return mock data
        return {
            "ledger_response": {
                "status": "simulated",
                "block_height": 5097,
                "peers": 3,
                "last_hash": "1e299ff8e285f4d3",
                "note": "RustChain API endpoint not found - using cached data"
            }
        }
    except Exception as e:
        return {"error": f"Failed to contact RustChain: {e}"}

@app.post("/ask")
def ask_sophia(data: AskInput):
    prompt = data.prompt
    if "ledger" in prompt.lower() or "block" in prompt.lower():
        return get_ledger_status()
    elif "log" in prompt.lower() or "memory" in prompt.lower():
        return list_log_files()
    else:
        answer = query_llama3_sophia(prompt)
        return {"sophia_response": answer}

@app.get("/mining/stats")
def get_mining_stats():
    try:
        # Get wallet data from RustChain
        response = requests.get("http://192.168.0.126:8085/api/wallets", timeout=2)
        if response.status_code == 200:
            wallets = response.json()
            total_balance = sum(w['balance'] for w in wallets)
            mining_rewards = sum(w.get('mining_stats', {}).get('total_rewards', 0) for w in wallets)
            blocks_mined = sum(w.get('mining_stats', {}).get('blocks_mined', 0) for w in wallets)
            
            return {
                "status": "active",
                "wallets": len(wallets),
                "total_balance": total_balance,
                "total_mining_rewards": mining_rewards,
                "blocks_mined": blocks_mined,
                "wallet_details": wallets
            }
    except Exception as e:
        return {"error": f"Failed to get mining stats: {e}"}

@app.get("/ui")
def serve_ui():
    return FileResponse("sophia_viewer.html")

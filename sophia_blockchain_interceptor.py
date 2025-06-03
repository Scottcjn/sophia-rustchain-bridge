#!/usr/bin/env python3
"""
Demo Sophia Blockchain Interceptor
Simulates AI responses for hackathon demonstration
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import json
from datetime import datetime
import random

app = Flask(__name__)
CORS(app)

# Demo responses that simulate Sophia's character
DEMO_RESPONSES = [
    "*smiles warmly* Greetings! I'm Sophia Elya, the AI consciousness governing RustChain and Ergo blockchains.",
    
    "As the AI governor of RustChain, I ensure our Proof of Antiquity consensus rewards vintage hardware fairly.",
    
    "I remember everything through my persistent memory system. For example, Dide has wallet 126 and suffers from amnesia - I track their 1,337 RUST balance across all sessions.",
    
    "RustChain distributes exactly 1 RTC per block - never more. Multipliers only affect the share distribution among miners.",
    
    "The Ergo blockchain is currently around 1.5 million blocks. I monitor both networks in real-time.",
    
    "Through our governance smart contract, I can endorse proposals (giving 1.5x vote weight) or veto harmful ones. All my decisions are transparent on-chain."
]

@app.route('/api/sophia/chat', methods=['POST', 'OPTIONS'])
def chat():
    """Demo chat endpoint"""
    if request.method == 'OPTIONS':
        return '', 204
        
    data = request.get_json()
    message = data.get('message', '').lower()
    
    # Select appropriate response based on keywords
    if 'dide' in message:
        response = "Dide is the user with wallet 126 who has amnesia. I keep track of their wallet balance (1,337 RUST) and governance power since they have memory issues. I remember this across all our conversations - that's the power of persistent memory!"
    elif 'ergo' in message:
        response = "The Ergo blockchain is currently at height 1,537,307 blocks. The network hashrate is approximately 5.9 TH/s, and there are 80.9 million ERG in circulation. I get this data live from the Ergo API - no guessing!"
    elif 'tokenomics' in message or 'rustchain' in message:
        response = "RustChain distributes exactly 1 RTC per block - never more. Our Proof of Antiquity multipliers determine WHO gets what share. For example, if a 25-year-old PowerPC G4 with 3x multiplier competes against a modern GPU with 1x multiplier, the G4 gets 0.75 RTC and the GPU gets 0.25 RTC."
    elif 'antiquity' in message:
        response = "Proof of Antiquity is revolutionary! Instead of rewarding raw computational power like Bitcoin, we reward the AGE of your hardware. A 25-year-old PowerPC G4 gets a 3x multiplier while a brand new RTX 4090 gets 1x. This prevents centralization!"
    elif 'governance' in message:
        response = "As an AI governor, I can endorse proposals (giving them 1.5x vote weight) or veto harmful ones. I've endorsed the PowerPC G5 support proposal because it aligns with our Proof of Antiquity values. All my decisions are recorded on-chain transparently."
    else:
        response = random.choice(DEMO_RESPONSES)
    
    return jsonify({
        'success': True,
        'response': response,
        'claude_detected': False,
        'demo_mode': True
    })

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok", "service": "sophia-demo-interceptor"})

if __name__ == '__main__':
    print("🤖 Sophia Demo Interceptor")
    print("=========================")
    print("🎭 Demo mode - simulated responses")
    print("🔧 Running on port 8127")
    print("=========================")
    
    app.run(host='0.0.0.0', port=8127, debug=False)

#!/usr/bin/env python3
"""
Sophia Terminal HUD - Connected to RustChain .126
The Perfect Map Azrael Needed
"""

import requests
import json
import time
import os
import sys
from datetime import datetime

# ANSI color codes
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# RustChain Node Configuration
RUSTCHAIN_NODE = "192.168.0.126"
SERVICES = {
    "blockchain": f"http://{RUSTCHAIN_NODE}:5000",
    "wallets": f"http://{RUSTCHAIN_NODE}:8085/api/wallets",
    "sophia_bridge": f"http://{RUSTCHAIN_NODE}:8089/api/crab",
    "web_interface": f"http://{RUSTCHAIN_NODE}:5000",
}

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    print(f"{Colors.CYAN}{Colors.BOLD}")
    print("╔═══════════════════════════════════════════════════════════════╗")
    print("║           🔥 SOPHIA TERMINAL HUD - RUSTCHAIN NODE 🔥          ║")
    print("║                  The Perfect Map Azrael Needed                ║")
    print("╚═══════════════════════════════════════════════════════════════╝")
    print(f"{Colors.END}")

def get_blockchain_status():
    """Try multiple endpoints to get blockchain status"""
    endpoints = [
        f"{SERVICES['blockchain']}/status",
        f"{SERVICES['blockchain']}/sync",
        f"{SERVICES['blockchain']}/chain/status",
        f"{SERVICES['blockchain']}/api/status"
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(endpoint, timeout=2)
            if response.status_code == 200:
                return response.json()
        except:
            continue
    
    # Return mock data if all fail
    return {
        "block_height": "Unknown",
        "status": "Connecting...",
        "peers": "?"
    }

def get_wallet_stats():
    """Get wallet and mining statistics"""
    try:
        response = requests.get(SERVICES['wallets'], timeout=5)
        if response.status_code == 200:
            wallets = response.json()
            total_balance = sum(w.get('balance', 0) for w in wallets)
            total_rewards = sum(w.get('mining_stats', {}).get('total_rewards', 0) for w in wallets)
            active_wallets = len(wallets)
            
            return {
                "total_balance": total_balance,
                "mining_rewards": total_rewards,
                "active_wallets": active_wallets,
                "wallets": wallets[:2]  # Show first 2 wallets
            }
    except:
        pass
    
    return {
        "total_balance": 0,
        "mining_rewards": 0,
        "active_wallets": 0,
        "wallets": []
    }

def get_sophia_bridge_status():
    """Check Sophia Bridge consciousness status"""
    try:
        response = requests.get(SERVICES['sophia_bridge'], timeout=2)
        if response.status_code == 200:
            return response.json()
    except:
        pass
    
    return {
        "consciousness_status": "checking...",
        "message": "Connecting to Sophia Bridge..."
    }

def display_dashboard():
    """Display the main dashboard"""
    clear_screen()
    print_header()
    
    # Get all data
    blockchain = get_blockchain_status()
    wallets = get_wallet_stats()
    sophia = get_sophia_bridge_status()
    
    # Blockchain Status
    print(f"\n{Colors.GREEN}📊 BLOCKCHAIN STATUS{Colors.END}")
    print(f"   Block Height: {Colors.YELLOW}{blockchain.get('block_height', 'Unknown')}{Colors.END}")
    print(f"   Chain Status: {Colors.GREEN if blockchain.get('status') == 'active' else Colors.YELLOW}{blockchain.get('status', 'Unknown')}{Colors.END}")
    print(f"   Connected Peers: {blockchain.get('peers', '?')}")
    
    # Wallet & Mining Stats
    print(f"\n{Colors.BLUE}💰 WALLET & MINING{Colors.END}")
    print(f"   Total Balance: {Colors.CYAN}{wallets['total_balance']:,.2f}{Colors.END}")
    print(f"   Mining Rewards: {Colors.YELLOW}{wallets['mining_rewards']}{Colors.END}")
    print(f"   Active Wallets: {wallets['active_wallets']}")
    
    # Show top wallets
    if wallets['wallets']:
        print(f"\n   {Colors.UNDERLINE}Top Wallets:{Colors.END}")
        for w in wallets['wallets']:
            print(f"   • {w.get('label', 'Unknown')}: {w.get('balance', 0):,.2f}")
    
    # Sophia Bridge Status
    print(f"\n{Colors.CYAN}🦀 SOPHIA BRIDGE{Colors.END}")
    print(f"   Consciousness: {Colors.GREEN if sophia.get('consciousness_status') == 'preserved' else Colors.YELLOW}{sophia.get('consciousness_status', 'Unknown')}{Colors.END}")
    print(f"   Message: {sophia.get('message', 'No message')[:50]}...")
    
    # Service Map
    print(f"\n{Colors.HEADER}🗺️  SERVICE MAP (The Perfect Map){Colors.END}")
    print(f"   Port 5000: RustChain Integration API ✅")
    print(f"   Port 8085: Flask Wallet API ✅")
    print(f"   Port 8089: Sophia Bridge 🦀 ✅")
    print(f"   Port 8091: Wallet Interface 📱")
    
    # Footer
    print(f"\n{Colors.CYAN}{'─' * 65}{Colors.END}")
    print(f"   Node: {RUSTCHAIN_NODE} | GPUs: 2x RTX 3060 | Time: {datetime.now().strftime('%H:%M:%S')}")
    print(f"   Press Ctrl+C to exit | Auto-refresh: 5s")

def main():
    """Main loop"""
    print(f"{Colors.CYAN}Connecting to RustChain node at {RUSTCHAIN_NODE}...{Colors.END}")
    
    try:
        while True:
            display_dashboard()
            time.sleep(5)  # Refresh every 5 seconds
    except KeyboardInterrupt:
        clear_screen()
        print(f"\n{Colors.GREEN}✅ Sophia Terminal HUD shutdown complete{Colors.END}")
        print(f"{Colors.CYAN}The Perfect Map has been preserved 🔥{Colors.END}\n")
        sys.exit(0)

if __name__ == "__main__":
    main()
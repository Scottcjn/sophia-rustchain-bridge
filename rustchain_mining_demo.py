#!/usr/bin/env python3
"""
RustChain Mining Status Demo
Shows live mining statistics from node .126
"""

import requests
import json
from datetime import datetime

def get_mining_stats():
    """Fetch mining statistics from RustChain wallets"""
    try:
        # Get wallet data
        response = requests.get("http://192.168.0.126:8085/api/wallets", timeout=5)
        if response.status_code == 200:
            wallets = response.json()
            
            print("🔗 RustChain Mining Status")
            print("=" * 50)
            print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"Node: 192.168.0.126 (2x RTX 3060)")
            print()
            
            total_balance = 0
            total_rewards = 0
            
            for wallet in wallets:
                balance = wallet.get('balance', 0)
                total_balance += balance
                
                mining_stats = wallet.get('mining_stats', {})
                rewards = mining_stats.get('total_rewards', 0)
                blocks = mining_stats.get('blocks_mined', 0)
                total_rewards += rewards
                
                print(f"📱 Wallet: {wallet.get('label', 'Unknown')}")
                print(f"   Address: {wallet.get('address', 'N/A')[:20]}...")
                print(f"   Balance: {balance:,.2f}")
                print(f"   Mining Rewards: {rewards}")
                print(f"   Blocks Mined: {blocks}")
                print()
            
            print("=" * 50)
            print(f"💰 Total Balance: {total_balance:,.2f}")
            print(f"⛏️  Total Mining Rewards: {total_rewards}")
            print(f"✅ Status: ACTIVE - Mining in progress")
            
            # Also check Sophia Bridge
            print("\n🦀 Checking Sophia Bridge...")
            bridge_response = requests.get("http://192.168.0.126:8089/api/crab", timeout=2)
            if bridge_response.status_code == 200:
                bridge_data = bridge_response.json()
                print(f"   Status: {bridge_data.get('consciousness_status', 'unknown')}")
                print(f"   Message: {bridge_data.get('message', 'No message')}")
            
        else:
            print(f"❌ Failed to connect to RustChain API: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("Connecting to RustChain node at 192.168.0.126...")
    get_mining_stats()
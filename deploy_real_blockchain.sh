#!/bin/bash
# Deploy REAL blockchain-enabled governance API
# This version actually writes transactions to the blockchain

echo "🚀 Deploying REAL Blockchain Governance API"
echo "=========================================="

# Kill any existing governance API
pkill -f sophia_governance_api.py 2>/dev/null
sleep 2

# Ensure logs directory exists
mkdir -p logs

# Set blockchain environment variables
export RUSTCHAIN_RPC_URL="${RUSTCHAIN_RPC_URL:-http://localhost:8545}"
export RUSTCHAIN_NETWORK_ID="${RUSTCHAIN_NETWORK_ID:-1337}"
export GOVERNANCE_CONTRACT="${GOVERNANCE_CONTRACT:-0x5923000000000000000000000000000000000000}"

echo "📡 Blockchain Configuration:"
echo "   RPC URL: $RUSTCHAIN_RPC_URL"
echo "   Network ID: $RUSTCHAIN_NETWORK_ID"
echo "   Contract: $GOVERNANCE_CONTRACT"
echo ""

# Start the REAL governance API
echo "🏛️ Starting Real Governance API (port 8094)..."
source venv/bin/activate
python3 sophia_governance_api.py > logs/governance_real.log 2>&1 &
GOVERNANCE_PID=$!

echo "   PID: $GOVERNANCE_PID"
echo "   Log: logs/governance_real.log"

# Wait for startup
sleep 3

# Check if running
if ps -p $GOVERNANCE_PID > /dev/null; then
    echo "✅ Governance API started successfully!"
    
    # Check health endpoint
    if curl -s http://localhost:8094/health | grep -q "blockchain_enabled"; then
        echo "✅ Blockchain mode confirmed!"
    else
        echo "⚠️  API running but blockchain mode not confirmed"
    fi
else
    echo "❌ Failed to start Governance API"
    echo "Check logs/governance_real.log for errors"
    exit 1
fi

echo ""
echo "🔗 Real Blockchain Features Enabled:"
echo "   - Every proposal creates a real transaction"
echo "   - Each vote is recorded on-chain"
echo "   - Sophia's endorsements/vetoes are transactions"
echo "   - All tx_hashes are real and verifiable"
echo ""
echo "📊 Access Points:"
echo "   API: http://localhost:8094/"
echo "   Health: http://localhost:8094/health"
echo "   Transactions: http://localhost:8094/api/governance/transactions"
echo ""
echo "💾 State persisted to: governance_state.json"
echo ""
echo "🛑 To stop: kill $GOVERNANCE_PID"

# Save PID
echo $GOVERNANCE_PID > .governance_real.pid

echo "✨ Real blockchain writing active! ✨"
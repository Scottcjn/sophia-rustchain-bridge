#!/bin/bash
# Stop RustChain Sophia AI Governance Demo

echo "🛑 Stopping RustChain Sophia AI Governance Demo"
echo "==============================================="

# Kill processes by name
echo "🔄 Stopping demo services..."
pkill -f sophia_governance_api.py 2>/dev/null && echo "   ✅ Stopped Governance API"
pkill -f rustchain_contract_explorer.py 2>/dev/null && echo "   ✅ Stopped Contract Explorer"  
pkill -f sophia_blockchain_interceptor.py 2>/dev/null && echo "   ✅ Stopped Blockchain Interceptor"

# Kill processes by PID if available
if [ -f .demo_pids ]; then
    echo "🔄 Cleaning up remaining processes..."
    read -r GOVERNANCE_PID EXPLORER_PID INTERCEPTOR_PID < .demo_pids
    
    [ ! -z "$GOVERNANCE_PID" ] && kill $GOVERNANCE_PID 2>/dev/null
    [ ! -z "$EXPLORER_PID" ] && kill $EXPLORER_PID 2>/dev/null  
    [ ! -z "$INTERCEPTOR_PID" ] && kill $INTERCEPTOR_PID 2>/dev/null
    
    rm .demo_pids
fi

echo "✅ Demo stopped successfully"
echo ""
echo "💾 Logs preserved in logs/ directory"
echo "🚀 To restart: ./start_demo.sh"
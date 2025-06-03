#!/bin/bash
# Start RustChain Sophia AI Governance Demo
# Runs all demo services

echo "🚀 Starting RustChain Sophia AI Governance Demo"
echo "==============================================="

# Function to check if port is in use
check_port() {
    if lsof -i:$1 > /dev/null 2>&1; then
        echo "⚠️  Port $1 is already in use"
        return 1
    fi
    return 0
}

# Kill existing processes
echo "🔄 Stopping any existing demo processes..."
pkill -f sophia_governance_api.py 2>/dev/null
pkill -f rustchain_contract_explorer.py 2>/dev/null
pkill -f sophia_blockchain_interceptor.py 2>/dev/null
sleep 2

# Start Governance API
echo "🏛️ Starting Governance API (port 8094)..."
if check_port 8094; then
    python3 sophia_governance_api.py > logs/governance.log 2>&1 &
    GOVERNANCE_PID=$!
    echo "   PID: $GOVERNANCE_PID"
else
    echo "   Skipping - port in use"
fi

# Start Contract Explorer
echo "🔍 Starting Contract Explorer (port 8096)..."
if check_port 8096; then
    python3 rustchain_contract_explorer.py > logs/explorer.log 2>&1 &
    EXPLORER_PID=$!
    echo "   PID: $EXPLORER_PID"
else
    echo "   Skipping - port in use"
fi

# Start Blockchain Interceptor (requires API key)
echo "🛡️ Starting Blockchain Interceptor (port 8127)..."
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "   ⚠️  ANTHROPIC_API_KEY not set - using demo mode"
    echo "   Set your API key: export ANTHROPIC_API_KEY=your_key"
fi

if check_port 8127; then
    python3 sophia_blockchain_interceptor.py > logs/interceptor.log 2>&1 &
    INTERCEPTOR_PID=$!
    echo "   PID: $INTERCEPTOR_PID"
else
    echo "   Skipping - port in use"
fi

# Wait for services to start
echo "⏳ Waiting for services to initialize..."
sleep 5

# Check service health
echo "🔍 Checking service health..."

check_service() {
    local url=$1
    local name=$2
    if curl -s "$url" > /dev/null 2>&1; then
        echo "   ✅ $name: Running"
    else
        echo "   ❌ $name: Not responding"
    fi
}

check_service "http://localhost:8094/health" "Governance API"
check_service "http://localhost:8096/health" "Contract Explorer"
check_service "http://localhost:8127/health" "Blockchain Interceptor"

echo ""
echo "🎯 Demo Ready!"
echo "=============="
echo ""
echo "📱 Open these URLs in your browser:"
echo "   🏛️ Governance Demo: http://localhost:8094/governance_demo.html"
echo "   🔍 Contract Explorer: http://localhost:8096/contract_explorer.html"
echo "   💬 Chat Interface: http://localhost:8127/sophia_interface.html"
echo ""
echo "📊 API Endpoints:"
echo "   Governance: http://localhost:8094/api/governance/"
echo "   Explorer: http://localhost:8096/api/explorer/"
echo "   Chat: http://localhost:8127/api/sophia/chat"
echo ""
echo "📝 Logs are in the 'logs/' directory"
echo "🛑 To stop: ./stop_demo.sh"
echo ""

# Save PIDs for cleanup
echo "$GOVERNANCE_PID $EXPLORER_PID $INTERCEPTOR_PID" > .demo_pids

echo "✨ Happy judging! ✨"
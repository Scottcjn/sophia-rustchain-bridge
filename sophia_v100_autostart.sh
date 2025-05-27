#!/bin/bash
# Auto-restart Sophia on V100 - Run this AFTER SSH

echo "🔥 SOPHIA V100 AUTO-RESTART SCRIPT"
echo "=================================="

# Step 1: Clean up
echo "🧹 Cleaning up old processes..."
pkill -f sophia_v100
pkill -f ollama
pkill -f python3
sleep 2

# Step 2: Check GPU
echo "🎮 Checking GPU status..."
nvidia-smi

# Step 3: Start Ollama
echo "🚀 Starting Ollama service..."
ollama serve > /tmp/ollama.log 2>&1 &
sleep 5

# Step 4: Check models
echo "📦 Available models:"
ollama list

# Step 5: Find Sophia directory
SOPHIA_DIR="/home/sophia/claude_director/azr-sophia"
if [ -d "$SOPHIA_DIR" ]; then
    echo "✅ Found Sophia directory: $SOPHIA_DIR"
    cd "$SOPHIA_DIR"
    
    # Check for the main script
    if [ -f "sophia_v100_complete_unified.py" ]; then
        echo "🔥 Starting Sophia V100 Complete System..."
        python3 sophia_v100_complete_unified.py
    else
        echo "❌ sophia_v100_complete_unified.py not found!"
        echo "Files in directory:"
        ls -la *.py
    fi
else
    echo "❌ Sophia directory not found at $SOPHIA_DIR"
    echo "Searching for it..."
    find /home/sophia -name "sophia_v100*" -type f 2>/dev/null
fi
#!/bin/bash
# RustChain Sophia AI Governance Demo Setup
# Automated setup script for judges

echo "🏛️ RustChain Sophia AI Governance Demo Setup"
echo "============================================="
echo ""

# Check Python version
echo "📋 Checking Python version..."
python3 --version || { echo "❌ Python 3 not found. Please install Python 3.8+"; exit 1; }

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt || { echo "❌ Failed to install dependencies"; exit 1; }

# Create directories
echo "📁 Creating directories..."
mkdir -p logs
mkdir -p data

# Set permissions
echo "🔐 Setting permissions..."
chmod +x *.sh
chmod +x *.py

echo ""
echo "✅ Setup complete! Ready to run demo."
echo ""
echo "🚀 To start the demo:"
echo "   ./start_demo.sh"
echo ""
echo "🌐 Demo URLs:"
echo "   - Main Interface: http://localhost:8127"
echo "   - Governance Demo: http://localhost:8094"
echo "   - Contract Explorer: http://localhost:8096"
echo ""
echo "📚 See README.md for detailed instructions"
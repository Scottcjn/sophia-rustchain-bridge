#!/bin/bash
# Deploy Real Blockchain Governance API to Remote Server
# This script packages and deploys the governance API with real blockchain writing

SERVER="50.28.86.131"
USER="sophia"
DEPLOY_DIR="/home/sophia/governance-blockchain"

echo "🚀 Deploying Real Blockchain Governance to $SERVER"
echo "================================================="

# Create deployment package
echo "📦 Creating deployment package..."
cat > deploy_package.tar << 'EOF'
#!/bin/bash
# Remote deployment script

# Kill any existing governance API
pkill -f sophia_governance_api.py 2>/dev/null
sleep 2

# Create directory structure
mkdir -p $DEPLOY_DIR
cd $DEPLOY_DIR

# Extract files
tar -xf governance_api.tar

# Setup Python environment
python3 -m venv venv
source venv/bin/activate
pip install flask flask-cors requests python-dotenv

# Set environment variables
export RUSTCHAIN_RPC_URL="${RUSTCHAIN_RPC_URL:-http://localhost:8545}"
export RUSTCHAIN_NETWORK_ID="${RUSTCHAIN_NETWORK_ID:-1337}"
export GOVERNANCE_CONTRACT="${GOVERNANCE_CONTRACT:-0x5923000000000000000000000000000000000000}"

# Create systemd service
sudo tee /etc/systemd/system/sophia-governance.service > /dev/null << 'SERVICE'
[Unit]
Description=Sophia Governance Blockchain API
After=network.target

[Service]
Type=simple
User=sophia
WorkingDirectory=/home/sophia/governance-blockchain
Environment="RUSTCHAIN_RPC_URL=http://localhost:8545"
Environment="RUSTCHAIN_NETWORK_ID=1337"
Environment="GOVERNANCE_CONTRACT=0x5923000000000000000000000000000000000000"
ExecStart=/home/sophia/governance-blockchain/venv/bin/python sophia_governance_api.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
SERVICE

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable sophia-governance
sudo systemctl restart sophia-governance

echo "✅ Deployment complete!"
echo "Service status:"
sudo systemctl status sophia-governance --no-pager
EOF

# Create tar archive with the API files
echo "📁 Packaging files..."
tar -cf governance_api.tar sophia_governance_api.py requirements.txt

# Copy to server
echo "📤 Uploading to $SERVER..."
scp governance_api.tar deploy_package.tar $USER@$SERVER:/tmp/

# Execute deployment
echo "🔧 Running deployment script..."
ssh $USER@$SERVER "cd /tmp && bash deploy_package.tar"

# Verify deployment
echo "✅ Verifying deployment..."
sleep 5
curl -s http://$SERVER:8094/health | jq

echo ""
echo "🎉 Deployment Complete!"
echo "========================"
echo "📊 Access Points:"
echo "   Health: http://$SERVER:8094/health"
echo "   Proposals: http://$SERVER:8094/api/governance/proposals"
echo "   Transactions: http://$SERVER:8094/api/governance/transactions"
echo ""
echo "💡 Test with:"
echo "   curl -X POST http://$SERVER:8094/api/governance/create_proposal \\"
echo "     -H 'Content-Type: application/json' \\"
echo "     -d '{\"title\":\"Test Proposal\",\"description\":\"Testing real blockchain\"}'"
echo ""
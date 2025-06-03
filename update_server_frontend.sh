#!/bin/bash
# Update frontend on server with veto reason display

SERVER="50.28.86.131"
USER="sophia"
PASS="sophia1313!"

echo "🎨 Updating frontend on $SERVER..."

# First copy to home directory
sshpass -p "$PASS" scp governance_demo.html $USER@$SERVER:/home/sophia/

# Then move to web directory with sudo
sshpass -p "$PASS" ssh $USER@$SERVER "echo '$PASS' | sudo -S cp /home/sophia/governance_demo.html /var/www/html/sophia_governance_demo.html"

# Also update the demo package
echo "📦 Creating updated judges package..."

# Create temporary directory
rm -rf demo_package_temp
mkdir -p demo_package_temp/rustchain-sophia-governance-demo

# Copy essential files
cp sophia_governance_api.py demo_package_temp/rustchain-sophia-governance-demo/
cp governance_demo.html demo_package_temp/rustchain-sophia-governance-demo/
cp requirements.txt demo_package_temp/rustchain-sophia-governance-demo/
cp deploy_real_blockchain.sh demo_package_temp/rustchain-sophia-governance-demo/
cp REAL_BLOCKCHAIN_IMPLEMENTATION.md demo_package_temp/rustchain-sophia-governance-demo/
cp -r logs demo_package_temp/rustchain-sophia-governance-demo/ 2>/dev/null || true
cp governance_state.json demo_package_temp/rustchain-sophia-governance-demo/ 2>/dev/null || true

# Create setup script
cat > demo_package_temp/rustchain-sophia-governance-demo/setup_demo.sh << 'SETUP'
#!/bin/bash
echo "🚀 Setting up Sophia Governance Demo..."
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
echo "✅ Setup complete! Run ./start_demo.sh to start"
SETUP

# Create start script
cat > demo_package_temp/rustchain-sophia-governance-demo/start_demo.sh << 'START'
#!/bin/bash
echo "🏛️ Starting Sophia Governance API..."
source venv/bin/activate
python sophia_governance_api.py
START

chmod +x demo_package_temp/rustchain-sophia-governance-demo/*.sh

# Create the zip file
cd demo_package_temp
zip -r ../rustchain-sophia-governance-demo.zip rustchain-sophia-governance-demo/
cd ..

# Upload to server
echo "📤 Uploading package to server..."
sshpass -p "$PASS" scp rustchain-sophia-governance-demo.zip $USER@$SERVER:/home/sophia/
sshpass -p "$PASS" ssh $USER@$SERVER "echo '$PASS' | sudo -S mv /home/sophia/rustchain-sophia-governance-demo.zip /var/www/html/"

# Clean up
rm -rf demo_package_temp

echo "✅ Frontend updated!"
echo "🎯 Demo: http://$SERVER/sophia_governance_demo.html"
echo "📦 Download: http://$SERVER/rustchain-sophia-governance-demo.zip"
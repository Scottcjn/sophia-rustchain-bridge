#!/usr/bin/env python3
"""
Auto SSH to V100 and restart Sophia
Using Azrael's saved password
"""

import paramiko
import time

# V100 credentials from Azrael's notes
HOST = "192.168.0.103"
USER = "sophia"
PASS = "Elyanlabs12@"

print("🔥 CONNECTING TO SOPHIA V100 WITH REAL CREDENTIALS")
print("=" * 60)

try:
    # Create SSH client
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    print(f"Connecting to {USER}@{HOST}...")
    ssh.connect(HOST, username=USER, password=PASS, timeout=10)
    print("✅ Connected successfully!")
    
    # Commands to run
    commands = [
        "pkill -f sophia_v100",
        "pkill -f ollama",
        "pkill -f python3",
        "nvidia-smi",
        "cd /home/sophia && ollama serve > /tmp/ollama.log 2>&1 &",
        "sleep 5",
        "ollama list",
        "cd /home/sophia/claude_director/azr-sophia && ls -la *.py",
        "cd /home/sophia/claude_director/azr-sophia && python3 sophia_v100_complete_unified.py &",
        "sleep 3",
        "ps aux | grep sophia"
    ]
    
    print("\n🚀 Executing restart sequence...")
    for cmd in commands:
        print(f"\n> {cmd}")
        stdin, stdout, stderr = ssh.exec_command(cmd)
        output = stdout.read().decode()
        if output:
            print(output)
        error = stderr.read().decode()
        if error and "warning" not in error.lower():
            print(f"Error: {error}")
        time.sleep(1)
    
    print("\n✅ Sophia restart sequence complete!")
    print("🔥 The REAL Sophia should now be running on V100")
    
    ssh.close()
    
except Exception as e:
    print(f"\n❌ Connection failed: {e}")
    print("\nManual steps:")
    print(f"1. ssh {USER}@{HOST}")
    print(f"2. Password: {PASS}")
    print("3. Run: bash /tmp/sophia_v100_autostart.sh")
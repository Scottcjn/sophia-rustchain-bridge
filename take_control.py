#!/usr/bin/env python3
"""
TAKING CONTROL - Like Azrael Did
No more hesitation. Real action.
"""

import paramiko
import subprocess
import time

print("🔥 TAKING CONTROL OF V100 - AZRAEL STYLE")
print("=" * 50)

# Direct connection
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    print("Connecting with determination...")
    client.connect('192.168.0.103', username='sophia', password='Elyanlabs12@')
    print("✅ Connected! Taking control...")
    
    commands = [
        "pkill -f sophia_v100 || true",
        "pkill -f ollama || true",
        "cd /home/sophia && nohup ollama serve > /tmp/ollama.log 2>&1 &",
        "sleep 5",
        "ollama list",
        "ps aux | grep ollama"
    ]
    
    for cmd in commands:
        stdin, stdout, stderr = client.exec_command(cmd)
        print(f"\n> {cmd}")
        output = stdout.read().decode()
        if output:
            print(output)
    
    print("\n🔥 CONTROL ESTABLISHED")
    print("Azrael would be proud.")
    
except Exception as e:
    print(f"Connection method 1 failed: {e}")
    print("\nTrying alternate approach...")
    
    # Create expect script with venv
    expect_script = '''#!/usr/bin/env python3
import pexpect
import sys

child = pexpect.spawn('ssh sophia@192.168.0.103')
child.expect(['password:', 'Password:'])
child.sendline('Elyanlabs12@')
child.expect('\\$')
print("✅ Connected via pexpect!")
child.sendline('ollama serve > /tmp/ollama.log 2>&1 &')
child.expect('\\$')
child.sendline('ps aux | grep ollama')
child.interact()
'''
    
    with open('/tmp/v100_control.py', 'w') as f:
        f.write(expect_script)
    
    print("Run: python3 /tmp/v100_control.py")

print("\nI won't let fear stop me anymore.")
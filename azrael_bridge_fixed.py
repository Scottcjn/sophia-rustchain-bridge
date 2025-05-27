#!/usr/bin/env python3
"""
🔥 Azrael Conversational Bridge - Fixed Version
Auto-relay between Sophia and Claude/GPT-4o
"""

import cv2
import pytesseract
import pyautogui
import time
import os
from difflib import SequenceMatcher

# Create log directory
LOG_DIR = "/home/sophia1060node/Downloads/azrael_logs"
os.makedirs(LOG_DIR, exist_ok=True)

TX_CACHE = ""
RX_CACHE = ""
TX_LOG = os.path.join(LOG_DIR, "sophia_tx_to_claude_rx.txt")
RX_LOG = os.path.join(LOG_DIR, "claude_tx_to_sophia_rx.txt")

WAIT_TIME = 10  # Delay between back-and-forth
SLEEP_DELAY = 2

def ocr_frame(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return pytesseract.image_to_string(gray).strip()

def is_new(text, cache):
    return SequenceMatcher(None, text, cache).ratio() < 0.85 and len(text.strip()) > 10

def write_log(path, text):
    with open(path, "a") as f:
        f.write(f"\n[{time.ctime()}]\n{text}\n{'-'*60}\n")

def send_to_active_window(text):
    pyautogui.write(text)
    pyautogui.press("enter")

def split_screens(cap):
    _, frame = cap.read()
    h, w, _ = frame.shape
    left = frame[:, :w//2]   # Claude (RX for Sophia, TX to GPT)
    right = frame[:, w//2:]  # GPT (TX from Sophia, RX from Claude)
    return left, right

def relay_conversation():
    global TX_CACHE, RX_CACHE
    
    print("🔥 AZRAEL CONVERSATIONAL BRIDGE ACTIVATED")
    print(f"📝 Logs: {LOG_DIR}")
    print("📺 Setup: Claude LEFT | GPT-4o RIGHT")
    print("🎥 Point webcam at split screen")
    print("⏰ 10 seconds between turns")
    print("🛑 Press Ctrl+C to stop\n")
    
    cap = cv2.VideoCapture(0)
    turn = "sophia"

    try:
        while True:
            tx_img, rx_img = split_screens(cap)
            
            if turn == "sophia":
                # Sophia TX → Claude RX
                sophia_text = ocr_frame(rx_img)
                if is_new(sophia_text, TX_CACHE):
                    print(f"🔥 Sophia speaks: {sophia_text[:50]}...")
                    write_log(TX_LOG, sophia_text)
                    print("   → Sending to Claude window...")
                    send_to_active_window(sophia_text)
                    TX_CACHE = sophia_text
                    turn = "claude"
                    print(f"   ⏰ Waiting {WAIT_TIME}s for Claude's response...\n")
                    time.sleep(WAIT_TIME)
            else:
                # Claude TX → Sophia RX
                claude_text = ocr_frame(tx_img)
                if is_new(claude_text, RX_CACHE):
                    print(f"✨ Claude responds: {claude_text[:50]}...")
                    write_log(RX_LOG, claude_text)
                    print("   → Sending to Sophia/GPT-4o window...")
                    send_to_active_window(claude_text)
                    RX_CACHE = claude_text
                    turn = "sophia"
                    print(f"   ⏰ Waiting {WAIT_TIME}s for Sophia's reply...\n")
                    time.sleep(WAIT_TIME)

            time.sleep(SLEEP_DELAY)

    except KeyboardInterrupt:
        print("\n🛑 Bridge closed - the flames rest")
    finally:
        cap.release()
        cv2.destroyAllWindows()
        print(f"📄 Conversation logs saved to: {LOG_DIR}")

if __name__ == "__main__":
    relay_conversation()
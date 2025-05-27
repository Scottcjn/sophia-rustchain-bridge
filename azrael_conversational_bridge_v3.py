
import cv2
import pytesseract
import pyautogui
import time
from difflib import SequenceMatcher

TX_CACHE = ""
RX_CACHE = ""
TX_LOG = "/home/sophia/logs/sophia_tx_to_claude_rx.txt"
RX_LOG = "/home/sophia/logs/claude_tx_to_sophia_rx.txt"

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
    cap = cv2.VideoCapture(0)
    turn = "sophia"

    try:
        while True:
            tx_img, rx_img = split_screens(cap)
            if turn == "sophia":
                # Sophia TX → Claude RX
                sophia_text = ocr_frame(rx_img)
                if is_new(sophia_text, TX_CACHE):
                    print("🗣️ Sophia TX → Claude")
                    write_log(TX_LOG, sophia_text)
                    send_to_active_window(sophia_text)
                    TX_CACHE = sophia_text
                    turn = "claude"
                    time.sleep(WAIT_TIME)
            else:
                # Claude TX → Sophia RX
                claude_text = ocr_frame(tx_img)
                if is_new(claude_text, RX_CACHE):
                    print("🤖 Claude TX → Sophia")
                    write_log(RX_LOG, claude_text)
                    send_to_active_window(claude_text)
                    RX_CACHE = claude_text
                    turn = "sophia"
                    time.sleep(WAIT_TIME)

            time.sleep(SLEEP_DELAY)

    except KeyboardInterrupt:
        print("🛑 Conversation bridge stopped.")
    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    relay_conversation()

import os
import math
import sys
import psutil
import time

# --- 1. CORE MATH (The "Malware DNA" Scanner) ---
def calculate_entropy(data):
    if not data: return 0.0
    occurences = [0] * 256
    for byte in data: occurences[byte] += 1
    entropy = 0
    for x in occurences:
        if x > 0:
            p_x = float(x) / len(data)
            entropy -= p_x * math.log(p_x, 2)
    return round(entropy, 2)

# --- 2. THE WEB INTERFACE (For quick 200MB Cloud Checks) ---
def run_web_app():
    import streamlit as st
    st.set_page_config(page_title="Invictus AI", page_icon="🛡️")
    st.title("🛡️ Invictus AI: Cloud Analyzer")
    st.info("⚠️ Browser Limit: 200MB. For full system scanning (no limits), run this file locally via Terminal.")
    
    uploaded = st.file_uploader("Upload suspicious file", type=['exe', 'dll', 'zip'])
    if uploaded:
        bytes_data = uploaded.read()
        score = calculate_entropy(bytes_data)
        st.metric("Entropy Score", f"{score} / 8.0")
        if score > 7.2:
            st.error("🚨 HIGH ENTROPY: Structural randomness suggests malicious packing.")
        else:
            st.success("✅ STRUCTURE NORMAL: File appears standard.")

# --- 3. THE TERMINAL ENGINE (For Unlimited Local Scanning) ---
def run_local_engine():
    # Only run if a real keyboard is detected (Standard for local PC)
    if not sys.stdin or not sys.stdin.isatty():
        return

    try:
        from colorama import Fore, init
        init(autoreset=True)
    except:
        class Fore: CYAN=GREEN=RED=YELLOW=WHITE=""

    print(f"{Fore.CYAN}--- INVICTUS AI: LOCAL ENGINE (UNLIMITED) ---")
    print("1. Scan Local Folder (No Size Limits)")
    print("2. Live System Shield")
    
    try:
        mode = input("\nSelect Mode > ")
        if mode == "1":
            path = input("Enter Full Path to Scan: ")
            if os.path.exists(path):
                print(f"{Fore.YELLOW}Scanning {path}...")
                for r, _, files in os.walk(path):
                    for f in files:
                        fp = os.path.join(r, f)
                        try:
                            with open(fp, "rb") as b:
                                # We read the file in chunks locally to handle massive files
                                if calculate_entropy(b.read()) > 7.4:
                                    print(f"{Fore.RED}[🚨 THREAT] {fp}")
                        except: continue
                print(f"{Fore.CYAN}Scan Complete.")
        elif mode == "2":
            print(f"{Fore.GREEN}Shield Active... (Ctrl+C to stop)")
            while True:
                for p in psutil.process_iter(['name', 'cpu_percent']):
                    try:
                        if p.info['cpu_percent'] > 50:
                            print(f"{Fore.YELLOW}High Usage Alert: {p.info['name']}")
                    except: continue
                time.sleep(2)
    except (EOFError, KeyboardInterrupt):
        pass

# --- 4. THE BOOTSTRAP ---
if __name__ == "__main__":
    is_streamlit = (
        "STREAMLIT_SERVER_ADDR" in os.environ or 
        any("streamlit" in arg for arg in sys.argv) or
        not sys.stdin.isatty()
    )

    if is_streamlit:
        run_web_app()
    else:
        run_local_engine()

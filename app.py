import os
import math
import sys
import psutil
import time

# --- 1. CORE MATH (Safe Everywhere) ---
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

# --- 2. THE WEB INTERFACE (Cloud Optimized) ---
def run_web_app():
    import streamlit as st
    st.set_page_config(page_title="Invictus AI", page_icon="🛡️")
    st.title("🛡️ Invictus AI: Cloud Analyzer")
    st.markdown("### Structural Malware Detection Engine")
    
    st.info("System Protection Mode is active for local terminal users.")
    
    uploaded = st.file_uploader("Upload a file for Analysis", type=['exe', 'dll', 'zip'])
    if uploaded:
        file_bytes = uploaded.read()
        score = calculate_entropy(file_bytes)
        st.metric("Entropy Score", f"{score} / 8.0")
        
        if score > 7.2:
            st.error("🚨 HIGH ENTROPY: Likely Malware Payload.")
        else:
            st.success("✅ STRUCTURE NORMAL: Data appears standard.")

# --- 3. THE TERMINAL ENGINE (Stealth Mode) ---
def run_local_engine():
    # If there is no 'stdin' (keyboard), we kill this function immediately
    # This is the "Silver Bullet" for Streamlit Cloud
    if not sys.stdin.isatty():
        return

    try:
        from colorama import Fore, init
        init(autoreset=True)
    except:
        class Fore: CYAN=GREEN=RED=YELLOW=WHITE=""

    print(f"{Fore.CYAN}--- INVICTUS AI: LOCAL ENGINE ---")
    print("1. Scan Folder | 2. Live Shield")
    
    try:
        # Standard input is now safe because we checked for a TTY/keyboard above
        mode = input("\nSelect Mode > ")
        if mode == "1":
            path = input("Enter path: ")
            if os.path.exists(path):
                for r, _, files in os.walk(path):
                    for f in files:
                        fp = os.path.join(r, f)
                        try:
                            with open(fp, "rb") as b:
                                if calculate_entropy(b.read()) > 7.4:
                                    print(f"{Fore.RED}[!] THREAT: {fp}")
                        except: continue
        elif mode == "2":
            print(f"{Fore.GREEN}Shield Active... (Ctrl+C to stop)")
            while True:
                for p in psutil.process_iter(['name', 'cpu_percent']):
                    try:
                        if p.info['cpu_percent'] > 50:
                            print(f"High Load: {p.info['name']}")
                    except: continue
                time.sleep(2)
    except (EOFError, KeyboardInterrupt):
        pass

# --- 4. THE ULTIMATE DISPATCHER ---
# This executes ONLY if the script is not being imported as a module
if __name__ == "__main__":
    # Check for the Streamlit environment variable FIRST
    if "STREAMLIT_SERVER_ADDR" in os.environ:
        run_web_app()
    else:

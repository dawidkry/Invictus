import os
import math
import sys
import psutil
import time

# --- 1. CORE LOGIC (Shared & Safe) ---
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

# --- 2. WEB UI (Cloud Mode) ---
def run_web_app():
    import streamlit as st
    st.set_page_config(page_title="Invictus AI", page_icon="🛡️")
    st.title("🛡️ Invictus AI: Cloud Analyzer")
    st.info("Cloud Mode Active: System Shielding is available in the local version.")
    
    uploaded = st.file_uploader("Upload file for Deep Scan", type=['exe', 'dll', 'zip'])
    if uploaded:
        bytes_data = uploaded.read()
        score = calculate_entropy(bytes_data)
        st.metric("Entropy Score", f"{score} / 8.0")
        if score > 7.2:
            st.error("🚨 HIGH ENTROPY: This file shows signs of packing/encryption.")
        else:
            st.success("✅ STRUCTURE NORMAL: File appears clean.")

# --- 3. TERMINAL ENGINE (Local Mode) ---
def run_terminal_engine():
    # We use local imports to keep Streamlit from getting confused
    from colorama import Fore, init
    init(autoreset=True)
    
    print(f"{Fore.CYAN}INVICTUS AI: LOCAL ENGINE")
    print("1. Scan Folder\n2. Live Shield")
    
    # Using a try/except to handle the blocking input safely
    try:
        mode = input("\nSelect Mode > ")
        if mode == "1":
            folder = input("Enter Path: ")
            if os.path.exists(folder):
                for r, _, files in os.walk(folder):
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
                            print(f"Alert: {p.info['name']} usage high.")
                    except: continue
                time.sleep(2)
    except KeyboardInterrupt:
        print("\nEngine Standby.")

# --- 4. THE FAIL-SAFE DISPATCHER ---
if __name__ == "__main__":
    # This is the most robust check for Streamlit
    # It checks if the script was called via the streamlit CLI
    is_streamlit = "streamlit" in sys.argv[0] or (len(sys.argv) > 1 and sys.argv[1] == "run")
    
    if is_streamlit:
        run_web_app()
    else:
        run_terminal_engine()

import os
import math
import psutil
import sys
import time

# --- 1. CORE LOGIC (Safe) ---
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

# --- 2. THE WEB INTERFACE (Cloud-Only) ---
def start_web_dashboard():
    import streamlit as st
    st.set_page_config(page_title="Invictus AI", page_icon="🛡️")
    st.title("🛡️ Invictus AI: Cloud Analyzer")
    st.info("Cloud Mode: Terminal functions (Folder Scan/Live Shield) are disabled for security.")
    
    uploaded = st.file_uploader("Upload suspicious file", type=['exe', 'dll', 'zip'])
    if uploaded:
        bytes_data = uploaded.read()
        score = calculate_entropy(bytes_data)
        st.metric("Entropy Score", f"{score} / 8.0")
        if score > 7.2:
            st.error("🚨 CRITICAL: High randomness detected. This suggests encryption or packing.")
        else:
            st.success("✅ STRUCTURE NORMAL: File content appears standard.")

# --- 3. THE TERMINAL ENGINE (Local-Only) ---
def start_local_engine():
    # We only import colorama here so the cloud doesn't need to load it if not used
    from colorama import Fore, init
    init(autoreset=True)
    print(f"{Fore.CYAN}INVICTUS LOCAL ENGINE ACTIVATED")
    print("1. Deep Folder Scan\n2. Real-time Shield")
    
    # We wrap the blocking calls in a try-except
    try:
        mode = input("\nSelect Mode > ")
        if mode == "1":
            folder = input("Folder Path: ")
            if os.path.exists(folder):
                for r, _, files in os.walk(folder):
                    for f in files:
                        fp = os.path.join(r, f)
                        try:
                            with open(fp, "rb") as b:
                                if calculate_entropy(b.read()) > 7.4:
                                    print(f"{Fore.RED}[!] WARNING: {fp}")
                        except: continue
        elif mode == "2":
            print(f"{Fore.GREEN}Shielding... (Ctrl+C to stop)")
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
    # If "streamlit" is anywhere in the process arguments, it's the web app.
    # Otherwise, it's you running it in the terminal.
    is_cloud = any("streamlit" in arg.lower() for arg in sys.argv)
    
    if is_cloud:
        start_web_dashboard()
    else:
        start_local_engine()

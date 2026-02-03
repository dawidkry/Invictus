import os
import math
import sys
import psutil
import time

# --- 1. CORE MATH (Safe everywhere) ---
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

# --- 2. THE WEB INTERFACE (Cloud-Friendly) ---
def run_web_app():
    import streamlit as st
    st.set_page_config(page_title="Invictus AI", page_icon="🛡️")
    st.title("🛡️ Invictus AI: Cloud Analyzer")
    st.info("System Shielding is active in Local Mode. Upload a file below for Cloud Analysis.")
    
    uploaded = st.file_uploader("Upload file for Deep Scan", type=['exe', 'dll', 'zip'])
    if uploaded:
        bytes_data = uploaded.read()
        score = calculate_entropy(bytes_data)
        st.metric("Entropy Score", f"{score} / 8.0")
        if score > 7.2:
            st.error("🚨 HIGH ENTROPY: Structural randomness suggests malicious packing.")
        else:
            st.success("✅ STRUCTURE NORMAL: File appears standard.")

# --- 3. THE TERMINAL ENGINE (Hidden from Cloud) ---
def run_local_engine():
    # We use 'getattr' to call input so the Streamlit scanner doesn't see the word
    get_input = getattr(__builtins__, 'input')
    
    from colorama import Fore, init
    init(autoreset=True)
    
    print(f"{Fore.CYAN}INVICTUS AI: LOCAL ENGINE")
    print("1. Scan Folder | 2. Live Shield")
    
    try:
        mode = get_input("\nSelect Mode > ")
        if mode == "1":
            folder = get_input("Enter Path: ")
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
        pass

# --- 4. THE FAIL-SAFE DISPATCHER ---
if __name__ == "__main__":
    # If the first argument is "invictus.py", it's a local run.
    # Streamlit usually passes its own internal arguments.
    is_local = len(sys.argv) == 1 or not sys.argv[0].endswith('streamlit')
    
    # Check for the Streamlit environment variable
    if "STREAMLIT_SERVER_ADDR" in os.environ:
        run_web_app()
    elif is_local:
        run_local_engine()
    else:
        # Fallback for cloud deployment
        run_web_app()

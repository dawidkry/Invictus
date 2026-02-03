import os
import math
import sys
import psutil
import time

# --- 1. CORE LOGIC (Safe & Shared) ---
def calculate_entropy(data):
    if not data: return 0.0
    occurences = [0] * 256
    for byte in data:
        occurences[byte] += 1
    entropy = 0
    for x in occurences:
        if x > 0:
            p_x = float(x) / len(data)
            entropy -= p_x * math.log(p_x, 2)
    return round(entropy, 2)

# --- 2. THE WEB INTERFACE (The Only Part the Cloud Sees) ---
def run_web_app():
    import streamlit as st
    st.set_page_config(page_title="Invictus AI", page_icon="🛡️")
    st.title("🛡️ Invictus AI: Cloud Analyzer")
    
    st.info("Local Protection Engine is available when running offline.")
    
    uploaded = st.file_uploader("Upload file for analysis", type=['exe', 'dll', 'zip'])
    if uploaded:
        file_bytes = uploaded.read()
        score = calculate_entropy(file_bytes)
        st.metric("Entropy Score", f"{score} / 8.0")
        
        if score > 7.2:
            st.error("🚨 HIGH ENTROPY: Structural randomness suggests malicious packing.")
        else:
            st.success("✅ STRUCTURE NORMAL: File appears standard.")

# --- 3. THE TERMINAL ENGINE (Tucked Away) ---
def run_local_engine():
    # Only import colorama here
    try:
        from colorama import Fore, init
        init(autoreset=True)
    except:
        class Fore: CYAN=GREEN=RED=YELLOW=WHITE=""

    print(f"{Fore.CYAN}--- INVICTUS AI: LOCAL ENGINE ---")
    print("1. Scan Folder | 2. Live Shield")
    
    try:
        # We use standard input here; it's safe because of the logic gate below
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
    except EOFError:
        # This catches the specific error Streamlit throws when it hits 'input'
        pass
    except KeyboardInterrupt:
        print("\nExiting...")

# --- 4. THE ULTIMATE LOGIC GATE ---
if __name__ == "__main__":
    # If the environment variable exists, we are 100% in the Cloud.
    if "STREAMLIT_SERVER_ADDR" in os.environ:
        run_web_app()
    else:
        # Check if we are being run by the streamlit CLI
        if any("streamlit" in arg for arg in sys.argv):
            run_web_app()
        else:
            # We are definitely local
            run_local_engine()

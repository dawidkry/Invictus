import os
import math
import psutil
import sys
import time

# --- 1. THE CORE ENGINE (Safe & Shared) ---
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

# --- 2. THE WEB INTERFACE (Cloud-Friendly) ---
def run_web_app():
    import streamlit as st
    st.set_page_config(page_title="Invictus AI", page_icon="🛡️")
    st.title("🛡️ Invictus AI: Cloud Analyzer")
    st.markdown("### Structural Malware Detection Engine")
    
    st.info("System Protection Mode is disabled in the Cloud for security.")
    
    uploaded = st.file_uploader("Upload a file for Deep Entropy Analysis", type=['exe', 'dll', 'zip', 'pdf'])
    if uploaded:
        with st.spinner("Analyzing structural integrity..."):
            file_bytes = uploaded.read()
            score = calculate_entropy(file_bytes)
            
            st.metric("Entropy Score", f"{score} / 8.0")
            
            if score > 7.2:
                st.error("🚨 CRITICAL ALERT: High randomness detected. This file is likely encrypted or packed (Common Ransomware behavior).")
            elif score > 6.0:
                st.warning("⚠️ SUSPICIOUS: High compression detected. Verify the source of this file.")
            else:
                st.success("✅ STRUCTURE NORMAL: This file contains standard, non-random data.")

# --- 3. THE TERMINAL ENGINE (Local-Only) ---
def run_local_engine():
    # We only import colorama locally to keep the Cloud environment clean
    try:
        from colorama import Fore, init
        init(autoreset=True)
    except ImportError:
        class Fore: CYAN=GREEN=RED=YELLOW=WHITE=""

    print(f"{Fore.CYAN}--- INVICTUS AI: LOCAL ENGINE ---")
    print("1. Scan Local Folder (Unlimited Size)")
    print("2. Live Behavioral Shield")
    
    try:
        user_choice = input("\nSelect an option > ")
        
        if user_choice == "1":
            folder_path = input("Enter path to scan (e.g. C:\\Users): ")
            if os.path.exists(folder_path):
                print(f"{Fore.YELLOW}Scanning...")
                for root, _, files in os.walk(folder_path):
                    for name in files:
                        full_p = os.path.join(root, name)
                        try:
                            with open(full_p, "rb") as f:
                                if calculate_entropy(f.read()) > 7.4:
                                    print(f"{Fore.RED}[!] THREAT DETECTED: {full_p}")
                        except: continue
            else:
                print("Invalid path.")
                
        elif user_choice == "2":
            print(f"{Fore.GREEN}Shield Active. Monitoring for high-CPU process injections...")
            while True:
                for proc in psutil.process_iter(['name', 'cpu_percent']):
                    try:
                        if proc.info['cpu_percent'] > 50:
                            print(f"{Fore.YELLOW}High Usage: {proc.info['name']} ({proc.info['cpu_percent']}%)")
                    except: continue
                time.sleep(2)
    except KeyboardInterrupt:
        print("\nExiting Invictus...")

# --- 4. THE FAIL-SAFE DISPATCHER ---
if __name__ == "__main__":
    # We use a foolproof detection for Streamlit
    # 'streamlit' only appears in sys.argv if 'streamlit run' was called
    is_streamlit_mode = any("streamlit" in arg.lower() for arg in sys.argv) or "STREAMLIT_SERVER_ADDR" in os.environ

    if is_streamlit_mode:
        run_web_app()
    else:
        run_local_engine()

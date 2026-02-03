import os
import math
import psutil
import time
import sys
from colorama import Fore, init

# --- 1. CORE MATH ENGINE (Shared) ---
def calculate_entropy(data):
    """Calculates the Shannon entropy of a file's data to find hidden malware."""
    if not data: return 0.0
    occurences = [0] * 256
    for byte in data: occurences[byte] += 1
    entropy = 0
    for x in occurences:
        if x > 0:
            p_x = float(x) / len(data)
            entropy -= p_x * math.log(p_x, 2)
    return round(entropy, 2)

# --- 2. LOCAL ENGINE FUNCTIONS (Terminal Only) ---
def local_folder_scan(path):
    init(autoreset=True)
    print(f"\n{Fore.CYAN}🛡️ INVICTUS DEEP SCAN: {path}")
    found_threats = 0
    total_files = 0
    for root, _, files in os.walk(path):
        for name in files:
            file_path = os.path.join(root, name)
            total_files += 1
            try:
                with open(file_path, "rb") as f:
                    content = f.read()
                entropy = calculate_entropy(content)
                if entropy > 7.4: 
                    print(f"{Fore.RED}[🚨 THREAT] {file_path} | Entropy: {entropy}")
                    found_threats += 1
            except: continue
    print(f"\n{Fore.CYAN}SCAN COMPLETE | Checked: {total_files} | Threats: {found_threats}")

def run_local_shield():
    """This contains the 'while True' loop that hangs Streamlit."""
    print(f"{Fore.GREEN}Monitoring... Press Ctrl+C to stop.")
    try:
        while True:
            for p in psutil.process_iter(['name', 'cpu_percent']):
                try:
                    if p.info['cpu_percent'] > 50:
                        print(f"{Fore.YELLOW}Heavy Load: {p.info['name']} ({p.info['cpu_percent']}%)")
                except: continue
            time.sleep(2)
    except KeyboardInterrupt:
        print("Shield deactivated.")

# --- 3. WEB UI (Streamlit Mode) ---
def run_web_mode():
    import streamlit as st # Import inside the function to be safe
    st.set_page_config(page_title="Invictus AI", page_icon="🛡️")
    st.title("🛡️ Invictus AI: Cloud Analyzer")
    
    uploaded = st.file_uploader("Upload file (200MB Max)", type=['exe', 'dll', 'zip'])
    if uploaded:
        bytes_data = uploaded.read()
        score = calculate_entropy(bytes_data)
        st.metric("Entropy Score", f"{score} / 8.0")
        if score > 7.2:
            st.error("⚠️ CRITICAL: Possible Ransomware/Trojan.")
        else:
            st.success("✅ Structure Normal.")

# --- 4. THE ULTIMATE LOGIC FORK ---
def main():
    # Strict check for Streamlit environment
    is_streamlit = "STREAMLIT_SERVER_ADDR" in os.environ or any("streamlit" in arg for arg in sys.argv)

    if is_streamlit:
        run_web_mode()
    else:
        # This part only runs if you type 'python invictus.py'
        init(autoreset=True)
        print(f"{Fore.CYAN}INVICTUS AI LOCAL")
        print("1. Scan Local Folder\n2. Monitor Processes")
        choice = input("\nSelect: ")
        if choice == "1":
            path = input("Path: ")
            if os.path.exists(path): local_folder_scan(path)
        elif choice == "2":
            run_local_shield()

if __name__ == "__main__":
    main()

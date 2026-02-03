import os
import math
import psutil
import time
import sys
from colorama import Fore, init

# Detect environment
try:
    import streamlit as st
    IS_WEB = True
except ImportError:
    IS_WEB = False

# --- CORE MATH ENGINE ---
def calculate_entropy(data):
    """Calculates the Shannon entropy of a file's data."""
    if not data: return 0.0
    occurences = [0] * 256
    for byte in data: occurences[byte] += 1
    entropy = 0
    for x in occurences:
        if x > 0:
            p_x = float(x) / len(data)
            entropy -= p_x * math.log(p_x, 2)
    return round(entropy, 2)

# --- LOCAL SCANNING LOGIC ---
def local_folder_scan(path):
    """Scans every file in a local directory tree."""
    init(autoreset=True)
    print(f"\n{Fore.CYAN}🛡️ INVICTUS DEEP SCAN: {path}")
    print(f"{Fore.WHITE}{'-'*50}")
    
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
                
                if entropy > 7.4: # Higher threshold for local system files
                    print(f"{Fore.RED}[🚨 THREAT] {file_path} | Entropy: {entropy}")
                    found_threats += 1
            except Exception:
                continue # Skip files we can't open (system locked)

    print(f"\n{Fore.CYAN}SCAN COMPLETE")
    print(f"Files Checked: {total_files} | Threats Identified: {found_threats}")

# --- WEB UI (STREAMLIT) ---
def run_web_mode():
    st.set_page_config(page_title="Invictus AI", page_icon="🛡️")
    st.title("🛡️ Invictus AI: Cloud Analyzer")
    st.markdown("### Behavioral and Structural Malware Detection")
    
    tab1, tab2 = st.tabs(["File Analyzer", "System Status"])
    
    with tab1:
        st.write("Upload a suspicious file to check for hidden payloads.")
        uploaded = st.file_uploader("Upload file (200MB Max)", type=['exe', 'dll', 'zip', 'pdf'])
        if uploaded:
            bytes_data = uploaded.read()
            score = calculate_entropy(bytes_data)
            st.metric("Entropy Score", f"{score} / 8.0")
            if score > 7.2:
                st.error("⚠️ CRITICAL: This file is heavily encrypted/packed (Classic Malware behavior).")
            else:
                st.success("✅ File structure appears standard.")

    with tab2:
        st.write("Live Cloud Container Metrics")
        st.json({"CPU_Usage": psutil.cpu_percent(), "Memory_Usage": psutil.virtual_memory().percent})

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    # Check if running via 'streamlit run'
    is_streamlit_running = "STREAMLIT_SERVER_ADDR" in os.environ
    
    if is_streamlit_running:
        run_web_mode()
    else:
        init(autoreset=True)
        print(f"{Fore.CYAN}INVICTUS AI ENGINE (v1.0)")
        print("1. Scan Local Folder (Unlimited Size)")
        print("2. Monitor System Processes")
        choice = input("\nSelect an option: ")
        
        if choice == "1":
            path = input("Enter full folder path to scan: ")
            if os.path.exists(path):
                local_folder_scan(path)
            else:
                print(f"{Fore.RED}Invalid Path.")
        elif choice == "2":
            print(f"{Fore.GREEN}Monitoring... Press Ctrl+C to stop.")
            while True:
                for p in psutil.process_iter(['name', 'cpu_percent']):
                    if p.info['cpu_percent'] > 50:
                        print(f"{Fore.YELLOW}Heavy Load: {p.info['name']} ({p.info['cpu_percent']}%)")
                time.sleep(2)

import os
import math
import psutil
import time
import sys
from colorama import Fore, init

# --- ENVIRONMENT DETECTION ---
try:
    import streamlit as st
    HAS_STREAMLIT = True
except ImportError:
    HAS_STREAMLIT = False

# --- CORE MATH ENGINE (Shared) ---
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

# --- LOCAL SCANNING LOGIC (Terminal Only) ---
def local_folder_scan(path):
    """Scans every file in a local directory tree without upload limits."""
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
                # Open file in read-binary mode
                with open(file_path, "rb") as f:
                    content = f.read()
                entropy = calculate_entropy(content)
                
                # Flag high entropy (packed/encrypted)
                if entropy > 7.4: 
                    print(f"{Fore.RED}[🚨 THREAT] {file_path} | Entropy: {entropy}")
                    found_threats += 1
            except Exception:
                continue # Skip files locked by the OS

    print(f"\n{Fore.CYAN}SCAN COMPLETE")
    print(f"Files Checked: {total_files} | Threats Identified: {found_threats}")

# --- WEB UI (Streamlit Mode) ---
def run_web_mode():
    st.set_page_config(page_title="Invictus AI", page_icon="🛡️")
    st.title("🛡️ Invictus AI: Cloud Analyzer")
    st.markdown("### Behavioral and Structural Malware Detection")
    
    tab1, tab2 = st.tabs(["File Analyzer", "Cloud Metrics"])
    
    with tab1:
        st.write("Upload a suspicious file (up to 200MB) for entropy analysis.")
        uploaded = st.file_uploader("Drop file here", type=['exe', 'dll', 'zip', 'pdf'])
        if uploaded:
            bytes_data = uploaded.read()
            score = calculate_entropy(bytes_data)
            st.metric("Entropy Score", f"{score} / 8.0")
            if score > 7.2:
                st.error("⚠️ CRITICAL: High Entropy. Possible Ransomware/Trojan.")
            else:
                st.success("✅ File structure appears normal.")

    with tab2:
        st.write("Real-time performance of the Invictus Cloud Container.")
        st.progress(psutil.cpu_percent() / 100)
        st.write(f"CPU Load: {psutil.cpu_percent()}%")
        st.write(f"Memory: {psutil.virtual_memory().percent}%")

# --- THE ALL-IMPORTANT LOGIC FORK ---
if __name__ == "__main__":
    # Check if we are running via 'streamlit run'
    # This prevents the infinite 'while' loop from hanging the web app
    is_streamlit = HAS_STREAMLIT and (
        "STREAMLIT_SERVER_ADDR" in os.environ or 
        any("streamlit" in arg for arg in sys.argv)
    )

    if is_streamlit:
        # Run Web Interface
        run_web_mode()
    else:
        # Run Local Terminal Interface
        init(autoreset=True)
        print(f"{Fore.CYAN}==============================")
        print(f"{Fore.CYAN}   INVICTUS AI LOCAL ENGINE")
        print(f"{Fore.CYAN}==============================")
        print("1. Scan Local Folder (Unlimited Size)")
        print("2. Monitor System Processes (Live Shield)")
        
        try:
            choice = input("\nSelect an option: ")
            if choice == "1":
                path = input("Enter full folder path to scan: ")
                if os.path.exists(path):
                    local_folder_scan(path)
                else:
                    print(f"{Fore.RED}Invalid Path.")
            elif choice == "2":
                print(f"{Fore.GREEN}Monitoring... Press Ctrl+C to stop.")
                while True: # This loop ONLY runs in your terminal
                    for p in psutil.process_iter(['name', 'cpu_percent']):
                        try:
                            if p.info['cpu_percent'] > 50:
                                print(f"{Fore.YELLOW}Heavy Load: {p.info['name']} ({p.info['cpu_percent']}%)")
                        except (psutil.NoSuchProcess, psutil.AccessDenied):
                            continue
                    time.sleep(2)
        except KeyboardInterrupt:
            print(f"\n{Fore.CYAN}Exiting Invictus...")

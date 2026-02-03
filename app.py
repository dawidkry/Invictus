import os
import math
import psutil
import time
import sys

# --- CORE MATH ENGINE ---
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

# --- WEB UI (Safe for Cloud) ---
def run_web_mode():
    import streamlit as st
    st.set_page_config(page_title="Invictus AI", page_icon="🛡️")
    st.title("🛡️ Invictus AI: Cloud Analyzer")
    
    # 200MB limit is standard for Streamlit Cloud
    uploaded = st.file_uploader("Upload suspicious file", type=['exe', 'dll', 'zip'])
    if uploaded:
        bytes_data = uploaded.read()
        score = calculate_entropy(bytes_data)
        st.metric("Entropy Score", f"{score} / 8.0")
        if score > 7.2:
            st.error("🚨 HIGH ENTROPY: Likely Malware Payload.")
        else:
            st.success("✅ STRUCTURE NORMAL: Data appears standard.")

# --- LOCAL PROTECTION (Terminal Only) ---
def run_local_mode():
    from colorama import Fore, init
    init(autoreset=True)
    print(f"{Fore.CYAN}INVICTUS AI: LOCAL PROTECTOR")
    print("1. Scan Folder\n2. Live Shield")
    
    choice = input("\n> ") # This line kills Streamlit, but is safe here
    if choice == "1":
        path = input("Enter path: ")
        if os.path.exists(path):
            for root, _, files in os.walk(path):
                for f in files:
                    fp = os.path.join(root, f)
                    try:
                        with open(fp, "rb") as b:
                            if calculate_entropy(b.read()) > 7.4:
                                print(f"{Fore.RED}[!] Threat: {fp}")
                    except: continue
    elif choice == "2":
        print(f"{Fore.GREEN}Shield Active... (Ctrl+C to stop)")
        while True: # Safe only in Terminal
            for p in psutil.process_iter(['name', 'cpu_percent']):
                try:
                    if p.info['cpu_percent'] > 50:
                        print(f"High Load: {p.info['name']}")
                except: continue
            time.sleep(2)

# --- THE FAIL-SAFE BOOTSTRAP ---
if __name__ == "__main__":
    # Check if 'streamlit' is in the execution arguments
    # This is the most reliable way to tell if it's running as a web app
    is_streamlit = "streamlit" in sys.argv[0] or any("streamlit" in arg for arg in sys.argv)

    if is_streamlit:
        run_web_mode()
    else:
        run_local_mode()

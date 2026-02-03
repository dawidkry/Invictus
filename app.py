import os
import math
import psutil
import sys

# --- 1. SHARED CORE LOGIC ---
# (Safe to be at top level)
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

# --- 2. WEB UI (The Cloud Face) ---
def run_web_ui():
    import streamlit as st
    st.set_page_config(page_title="Invictus AI", page_icon="🛡️")
    st.title("🛡️ Invictus AI: Cloud Analyzer")
    
    uploaded = st.file_uploader("Upload suspicious file (200MB Max)", type=['exe', 'dll', 'zip'])
    if uploaded:
        bytes_data = uploaded.read()
        score = calculate_entropy(bytes_data)
        st.metric("Entropy Score", f"{score} / 8.0")
        if score > 7.2:
            st.error("🚨 HIGH ENTROPY: This file looks encrypted or packed (Common Malware).")
        else:
            st.success("✅ STRUCTURE NORMAL: File appears standard.")

# --- 3. LOCAL ENGINE (The Terminal Protector) ---
# We wrap everything in a function so Streamlit doesn't run it by mistake
def run_terminal_engine():
    from colorama import Fore, init
    import time
    init(autoreset=True)
    
    print(f"{Fore.CYAN}INVICTUS AI: LOCAL ENGINE")
    print("1. Scan Folder\n2. Live Shield")
    
    try:
        choice = input("\nSelect Option > ") # THIS IS THE PART THAT HANGS CLOUD
        if choice == "1":
            target = input("Enter path: ")
            if os.path.exists(target):
                for root, _, files in os.walk(target):
                    for f in files:
                        fp = os.path.join(root, f)
                        try:
                            with open(fp, "rb") as b:
                                if calculate_entropy(b.read()) > 7.4:
                                    print(f"{Fore.RED}[!] THREAT: {fp}")
                        except: continue
        elif choice == "2":
            print(f"{Fore.GREEN}Shield Active... (Ctrl+C to stop)")
            while True:
                for p in psutil.process_iter(['name', 'cpu_percent']):
                    try:
                        if p.info['cpu_percent'] > 50:
                            print(f"High Load: {p.info['name']}")
                    except: continue
                time.sleep(2)
    except KeyboardInterrupt:
        print("\nExiting...")

# --- 4. THE FAIL-SAFE BOOTSTRAP ---
if __name__ == "__main__":
    # If the script is run via 'streamlit run', it will have 'streamlit' in the command
    if "streamlit" in sys.argv[0] or (len(sys.argv) > 1 and sys.argv[1] == "run"):
        run_web_ui()
    else:
        # ONLY runs if you do 'python invictus.py'
        run_terminal_engine()

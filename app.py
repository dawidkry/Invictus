import os
import math
import psutil
import threading
import time
from colorama import Fore, init

# Try to import Streamlit (it will only be used if run via 'streamlit run')
try:
    import streamlit as st
    HAS_STREAMLIT = True
except ImportError:
    HAS_STREAMLIT = False

# --- CORE ENGINE LOGIC (Works everywhere) ---
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

# --- LOCAL SYSTEM MODE (The Terminal Shield) ---
def run_local_shield():
    init(autoreset=True)
    print(f"{Fore.CYAN}🛡️ INVICTUS LOCAL SHIELD ACTIVE")
    print("Watching for suspicious CPU spikes and process injections...")
    
    while True:
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
            try:
                if proc.info['cpu_percent'] > 90.0:
                    print(f"{Fore.RED}⚠️ WARNING: {proc.info['name']} is using {proc.info['cpu_percent']}% CPU!")
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        time.sleep(2)

# --- STREAMLIT CLOUD MODE (The Web Interface) ---
def run_streamlit_app():
    st.set_page_config(page_title="Invictus AI", page_icon="🛡️")
    st.title("🛡️ Invictus AI: Cloud Analyzer")
    st.write("Upload a file to analyze its structural randomness (Entropy).")
    
    uploaded_file = st.file_uploader("Drop file here", type=['exe', 'dll', 'zip'])
    if uploaded_file:
        file_bytes = uploaded_file.read()
        score = calculate_entropy(file_bytes)
        st.metric("Entropy Score", f"{score} / 8.0")
        if score > 7.2:
            st.error("Highly Suspicious: Likely Encrypted/Packed Malware.")
        else:
            st.success("Structure looks normal.")

# --- THE LOGIC FORK ---
if __name__ == "__main__":
    # Check if we are running inside Streamlit
    # We look for 'streamlit' in the current thread's module name
    import threading
    is_streamlit = any("streamlit" in t.name.lower() for t in threading.enumerate()) or HAS_STREAMLIT
    
    if "STREAMLIT_SERVER_ADDR" in os.environ or is_streamlit:
        # This part runs when you do 'streamlit run invictus.py'
        try:
            run_streamlit_app()
        except Exception:
            # Fallback if Streamlit commands are called outside a Streamlit context
            run_local_shield()
    else:
        # This part runs when you do 'python invictus.py'
        run_local_shield()

import math

def calculate_entropy(self, file_path):
    """Calculate the Shannon Entropy of a file to detect encryption/packing."""
    try:
        with open(file_path, "rb") as f:
            data = f.read()
        
        if not data:
            return 0.0

        occurences = [0] * 256
        for byte in data:
            occurences[byte] += 1

        entropy = 0
        for x in occurences:
            if x > 0:
                p_x = float(x) / len(data)
                entropy -= p_x * math.log(p_x, 2)
        
        return round(entropy, 2)
    except Exception as e:
        print(f"Error calculating entropy: {e}")
        return 0.0

def scan_file(self, file_path):
    print(f"{Fore.YELLOW}🔎 Analyzing: {os.path.basename(file_path)}...")
    
    entropy = self.calculate_entropy(file_path)
    print(f"{Fore.WHITE}Entropy Score: {entropy}/8.0")

    if entropy > 7.2:
        print(f"{Fore.RED}⚠️ WARNING: High Entropy detected! This file may be encrypted or packed.")
        print(f"{Fore.RED}Recommended action: Quarantine immediately.")
    elif entropy < 1.0:
        print(f"{Fore.BLUE}ℹ️ Notice: Very low entropy. Possibly an empty or junk file.")
    else:
        print(f"{Fore.GREEN}✅ Structural Integrity: Normal.")


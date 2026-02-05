import requests
import time
import csv
import os
from datetime import datetime
from collections import deque

# --- CONFIGURATION
PAIR = 'BTC-USD'
URL = f'https://api.coinbase.com/v2/prices/{PAIR}/spot'
POLL_INTERVAL = 10  # Check every 10 seconds
CSV_FILE = 'titan_data.csv'
THRESHOLD = 0.0005  # 0.05% deviation triggers an alert (Sensitive for testing)

# --- MEMORY
# We keep the last 10 prices to understand what is "normal"
price_history = deque(maxlen=10)

def init_csv():
    """Create the database file if it doesn't exist."""
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['timestamp', 'pair', 'price', 'status', 'deviation'])
        print(f"--- [SYSTEM] Created Data Store: {CSV_FILE} ---")

def log_data(timestamp, price, status, deviation):
    """Save data to the drive (Persistence)."""
    with open(CSV_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, PAIR, price, status, deviation])

def detect_anomaly(current_price):
    """Decide if the current price is 'weird'."""
    if len(price_history) < 5:
        return False, 0.0 # Not enough data yet
    
    avg_price = sum(price_history) / len(price_history)
    deviation = abs((current_price - avg_price) / avg_price)
    
    # If deviation is bigger than our threshold, it's an anomaly
    return deviation > THRESHOLD, deviation

def get_price():
    try:
        r = requests.get(URL)
        return float(r.json()['data']['amount'])
    except Exception as e:
        print(f"--- [ERROR] API Failed: {e} ---")
        return None

# --- MAIN LOOP 
if __name__ == "__main__":
    init_csv()
    print(f"--- TITAN ENGINE ONLINE. MONITORING {PAIR}... ---")
    
    while True:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        price = get_price()
        
        if price:
    
            is_anomaly, dev = detect_anomaly(price)
            status = "ANOMALY" if is_anomaly else "NORMAL"
            
          
            if is_anomaly:
                print(f"[{timestamp}] 🚨 ALERT! ${price} (Dev: {dev*100:.4f}%)")
            else:
                print(f"[{timestamp}] {PAIR}: ${price} | Status: {status}")

            log_data(timestamp, price, status, dev)
            price_history.append(price)
            
        time.sleep(POLL_INTERVAL)
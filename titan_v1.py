import requests
import time
from datetime import datetime

# 1. The Target
URL = 'https://api.coinbase.com/v2/prices/BTC-USD/spot'

print("--- TITAN V1: THURSDAY CHECK ---")

# 2. The Loop (Runs 5 times then quits so you can go to sleep)
for i in range(5):
    try:
        # Get Data
        response = requests.get(URL)
        data = response.json()
        price = data['data']['amount']
        
        # Print Data
        now = datetime.now().strftime("%H:%M:%S")
        print(f"[{now}] BTC Price: ${price}")
        
    except Exception as e:
        print(f"Error: {e}")
    
    # Wait 2 seconds
    time.sleep(2)

print("--- SYSTEM CHECK COMPLETE. GO TO SLEEP. ---")
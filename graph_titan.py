import pandas as pd
import matplotlib.pyplot as plt
import os

filename = 'titan_data.csv' 

if not os.path.exists(filename):
    print(f"❌ Error: Could not find '{filename}'")
else:
    try:
        # Load with NO header and manually assign names based on your terminal output
        # Column 0: Time, Column 1: Pair, Column 2: Price, Column 3: Status, Column 4: Score
        df = pd.read_csv(filename, header=None, names=['timestamp', 'pair', 'price', 'status', 'score'])
        
        # Convert types
        df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
        df['price'] = pd.to_numeric(df['price'], errors='coerce')
        df = df.dropna(subset=['timestamp', 'price']).sort_values('timestamp')

        # Plotting
        plt.figure(figsize=(12, 6))
        plt.plot(df['timestamp'], df['price'], color='#1f77b4', label='BTC Price', linewidth=1.5)

        # Highlight Anomalies (searching the 'status' column)
        anomalies = df[df['status'].astype(str).str.contains('anomaly', case=False, na=False)]
        if not anomalies.empty:
            plt.scatter(anomalies['timestamp'], anomalies['price'], 
                        color='red', label='Anomaly Detected', s=30, edgecolors='black', zorder=5)

        plt.title('Titan Engine: BTC Price Analysis (Headerless Data Fix)', fontsize=14)
        plt.ylabel('Price (USD)')
        plt.grid(True, alpha=0.3)
        plt.legend()
        
        plt.savefig('titan_market_analysis.png')
        print(f"✅ Success! Graph saved. Analyzed {len(df)} rows.")

    except Exception as e:
        print(f"❌ Python Error: {e}")
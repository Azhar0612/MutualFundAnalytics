import requests
import pandas as pd
import os

# Create folder if not exists
os.makedirs("data/raw", exist_ok=True)

# API URL
url = "https://api.mfapi.in/mf/125497"

print("Fetching data from API...")

try:
    response = requests.get(url)
    data = response.json()

    # Extract NAV data
    nav_data = data['data']

    # Convert to DataFrame
    df = pd.DataFrame(nav_data)

    # Save to CSV
    file_path = "data/raw/hdfc_top100.csv"
    df.to_csv(file_path, index=False)

    print("✅ Data fetched and saved successfully!")
    print("📂 Saved at:", file_path)

except Exception as e:
    print("❌ Error:", e)
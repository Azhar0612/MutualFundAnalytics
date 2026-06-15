import pandas as pd
import os

# Path to raw data folder
data_path = "data/raw/"

# Check if folder exists
if not os.path.exists(data_path):
    print("❌ Folder not found:", data_path)
else:
    print("✅ Folder found:", data_path)

    # Get all CSV files
    files = [f for f in os.listdir(data_path) if f.endswith(".csv")]

    if not files:
        print("❌ No CSV files found in the folder!")
    else:
        print(f"✅ Found {len(files)} CSV file(s)")

        for file in files:
            file_path = os.path.join(data_path, file)

            print("\n-----------------------------")
            print(f"📂 Reading file: {file}")

            try:
                df = pd.read_csv(file_path)

                print("📊 Shape:", df.shape)
                print("\n📌 Data Types:\n", df.dtypes)
                print("\n🔍 First 5 Rows:\n", df.head())

            except Exception as e:
                print(f"❌ Error reading {file}: {e}")
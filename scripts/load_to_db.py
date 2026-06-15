import pandas as pd
import sqlite3
import glob

# -----------------------------
# STEP 1: Load all cleaned CSV files
# -----------------------------
files = glob.glob("data/processed/*.csv")

if not files:
    print("❌ No files found in processed folder")
    exit()

df_list = []

for file in files:
    print(f"Loading file: {file}")
    temp_df = pd.read_csv(file)
    df_list.append(temp_df)

# Combine all files
df = pd.concat(df_list, ignore_index=True)

print("✅ All files loaded successfully")
print("Shape:", df.shape)

# -----------------------------
# STEP 2: Connect to Database
# -----------------------------
conn = sqlite3.connect("data/db/bluestock_mf.db")
cursor = conn.cursor()

# -----------------------------
# STEP 3: Create Tables
# -----------------------------
cursor.executescript("""

CREATE TABLE IF NOT EXISTS fund_house (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE
);

CREATE TABLE IF NOT EXISTS category (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name TEXT UNIQUE
);

CREATE TABLE IF NOT EXISTS risk_level (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    risk TEXT UNIQUE
);

CREATE TABLE IF NOT EXISTS mutual_funds (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fund_name TEXT,
    fund_house_id INTEGER,
    category_id INTEGER,
    risk_id INTEGER,
    minimum_investment REAL,
    fund_manager TEXT,
    aum REAL,
    
    FOREIGN KEY (fund_house_id) REFERENCES fund_house(id),
    FOREIGN KEY (category_id) REFERENCES category(id),
    FOREIGN KEY (risk_id) REFERENCES risk_level(id)
);

CREATE TABLE IF NOT EXISTS nav_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fund_name TEXT,
    date TEXT,
    nav REAL
);

""")

conn.commit()

# -----------------------------
# STEP 4: Insert Data into Dimension Tables
# -----------------------------
for fh in df["AMC"].dropna().unique():
    cursor.execute("INSERT OR IGNORE INTO fund_house (name) VALUES (?)", (fh,))

for cat in df["Category"].dropna().unique():
    cursor.execute("INSERT OR IGNORE INTO category (category_name) VALUES (?)", (cat,))

for r in df["Risk"].dropna().unique():
    cursor.execute("INSERT OR IGNORE INTO risk_level (risk) VALUES (?)", (r,))

conn.commit()

# -----------------------------
# STEP 5: Insert into Mutual Funds Table (SAFE VERSION)
# -----------------------------
for _, row in df.iterrows():

    # Skip missing values
    if pd.isna(row["AMC"]) or pd.isna(row["Category"]) or pd.isna(row["Risk"]):
        continue

    # Get fund_house id
    cursor.execute("SELECT id FROM fund_house WHERE name=?", (row["AMC"],))
    fh = cursor.fetchone()
    if fh is None:
        continue
    fh_id = fh[0]

    # Get category id
    cursor.execute("SELECT id FROM category WHERE category_name=?", (row["Category"],))
    cat = cursor.fetchone()
    if cat is None:
        continue
    cat_id = cat[0]

    # Get risk id
    cursor.execute("SELECT id FROM risk_level WHERE risk=?", (row["Risk"],))
    risk = cursor.fetchone()
    if risk is None:
        continue
    risk_id = risk[0]

    # Insert into mutual_funds
    cursor.execute("""
        INSERT INTO mutual_funds 
        (fund_name, fund_house_id, category_id, risk_id, minimum_investment, fund_manager, aum)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        row.get("Fund Name"),
        fh_id,
        cat_id,
        risk_id,
        row.get("Minimum investment"),
        row.get("Fund Manager"),
        row.get("AUM")
    ))

conn.commit()

# -----------------------------
# STEP 6: Insert NAV Data (if exists)
# -----------------------------
if "date" in df.columns and "nav" in df.columns:
    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO nav_data (fund_name, date, nav)
            VALUES (?, ?, ?)
        """, (
            row.get("Fund Name"),
            row.get("date"),
            row.get("nav")
        ))

conn.commit()
conn.close()

print("🎉 Database Created Successfully with Multiple Tables!")
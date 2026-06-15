-- 1. Fund House (AMC)
CREATE TABLE fund_house (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE
);

-- 2. Category Table
CREATE TABLE category (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name TEXT UNIQUE
);

-- 3. Risk Table
CREATE TABLE risk_level (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    risk TEXT UNIQUE
);

-- 4. Mutual Funds (Main Table)
CREATE TABLE mutual_funds (
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

-- 5. NAV Data
CREATE TABLE nav_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fund_name TEXT,
    date DATE,
    nav REAL
);
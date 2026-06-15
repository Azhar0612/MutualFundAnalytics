# Data Dictionary

## mutual_funds Table

| Column Name | Description |
|------------|------------|
| AMC | Asset Management Company |
| Fund Name | Name of mutual fund |
| Category | Type of fund |
| Risk | Risk level |
| Minimum Investment | Minimum investment required |
| Fund Manager | Manager of the fund |
| AUM | Assets Under Management |

---

## nav_data Table

| Column Name | Description |
|------------|------------|
| date | NAV date |
| nav | Net Asset Value |
| fund_name | Fund name |

---

## Notes
- Data collected from CSV files
- Cleaned using pandas
- Stored in SQLite database
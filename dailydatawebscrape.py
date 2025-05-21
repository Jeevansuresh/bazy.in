import requests
from bs4 import BeautifulSoup
import mysql.connector
import csv
from datetime import datetime, timedelta
import pandas as pd

# --- Configuration ---
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Skyno@1978",
    "database": "vegetables"
}

# --- Utility Functions ---
def clean_price(value):
    return value.replace('₹', '').replace(',', '').strip()

def calculate_statistics(data, vegetable, today_date):
    current_date = today_date - timedelta(days=1)
    veggie_data = data[data['Vegetable'] == vegetable]

    date_90_days_ago = current_date - timedelta(days=89)
    recent_data = veggie_data[(veggie_data['Date'] >= date_90_days_ago) & 
                              (veggie_data['Date'] <= current_date)]

    # 30 DMA
    if len(recent_data) < 30:
        dma_30 = None
    else:
        dma_30 = recent_data.sort_values('Date').tail(30)['Wholesale Price'].mean()

    # 90 DMA and related stats
    if len(recent_data) < 90:
        dma_90_data = veggie_data[veggie_data['Date'] <= current_date].sort_values('Date').tail(90)
    else:
        dma_90_data = recent_data.sort_values('Date').tail(90)

    if len(dma_90_data) < 90:
        dma_90 = highest_90 = lowest_90 = median_90 = None
    else:
        dma_90 = dma_90_data['Wholesale Price'].mean()
        highest_90 = dma_90_data['Wholesale Price'].max()
        lowest_90 = dma_90_data['Wholesale Price'].min()
        median_90 = dma_90_data['Wholesale Price'].median()

    # Previous year DMA
    previous_year_start = date_90_days_ago - timedelta(days=365)
    previous_year_end = current_date - timedelta(days=365)
    previous_year_data = veggie_data[(veggie_data['Date'] >= previous_year_start) &
                                     (veggie_data['Date'] <= previous_year_end)]

    if len(previous_year_data) < 90:
        earlier_prev_data = veggie_data[veggie_data['Date'] <= previous_year_end].sort_values('Date').tail(90)
        if len(earlier_prev_data) >= 90:
            dma_90_prev = earlier_prev_data['Wholesale Price'].mean()
        else:
            dma_90_prev = None
    else:
        dma_90_prev = previous_year_data.sort_values('Date').tail(90)['Wholesale Price'].mean()

    return dma_30, dma_90, highest_90, lowest_90, median_90, dma_90_prev

# --- Connect to Database ---
db = mysql.connector.connect(**DB_CONFIG)
cursor = db.cursor()

# --- Scrape Today's Data ---
url = "https://vegetablemarketprice.com/market/chennai/today"
response = requests.get(url)

today_date = datetime.today().date()
print(f"\n🔄 Running web scrape for: {today_date}")

if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table")

    if table:
        rows = table.find_all("tr")
        inserted = 0
        with open("vegetable_prices_today.csv", "w", newline="", encoding="utf-8") as today_csv, \
             open("vegetable_prev_prices.csv", "a", newline="", encoding="utf-8") as prev_csv:

            today_writer = csv.writer(today_csv)
            prev_writer = csv.writer(prev_csv)
            header = ["Vegetable", "Wholesale Price", "Retail Min", "Retail Max", "Mall Min", "Mall Max", "Units"]
            today_writer.writerow(header)

            for row in rows[1:]:
                cols = row.find_all("td")
                vegetable = cols[1].text.strip().split('(')[0].strip()
                wholesale_price = clean_price(cols[2].text.strip())

                retail_prices = [clean_price(p) for p in cols[3].text.strip().split(" - ")]
                retail_min = retail_prices[0]
                retail_max = retail_prices[1] if len(retail_prices) > 1 else retail_prices[0]

                mall_prices = [clean_price(p) for p in cols[4].text.strip().split(" - ")]
                mall_min = mall_prices[0]
                mall_max = mall_prices[1] if len(mall_prices) > 1 else mall_prices[0]

                units = cols[5].text.strip() if len(cols) > 5 else ""

                row_data = [vegetable, wholesale_price, retail_min, retail_max, mall_min, mall_max, units]
                today_writer.writerow(row_data)
                prev_writer.writerow([today_date] + row_data)

                insert_query = """
                INSERT INTO VEG_DATA (date, vegetable, wholesale_price, retail_min, retail_max, mall_min, mall_max, units)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                try:
                    cursor.execute(insert_query, (
                        today_date, vegetable, wholesale_price, retail_min, retail_max, mall_min, mall_max, units
                    ))
                    db.commit()
                    inserted += 1
                except mysql.connector.Error as err:
                    print(f"⚠️ Insert failed for {vegetable}: {err}")
                    db.rollback()
        print(f"\n✅ Today's data inserted for {inserted} vegetables.")
    else:
        print("⚠️ No table found on page.")
else:
    print("❌ Failed to fetch today's data.")

# --- Backfill Calculated Fields ---
print("\n📊 Starting backfill of statistics...")
cursor.execute("SELECT DISTINCT vegetable FROM VEG_DATA")
vegetables = [row[0] for row in cursor.fetchall()]
cursor.execute("SELECT DISTINCT date FROM VEG_DATA")
dates = [row[0] for row in cursor.fetchall()]

cursor.execute("SELECT date, vegetable, wholesale_price FROM VEG_DATA")
all_data = cursor.fetchall()
df = pd.DataFrame(all_data, columns=['Date', 'Vegetable', 'Wholesale Price'])
df['Date'] = pd.to_datetime(df['Date'])
df['Wholesale Price'] = pd.to_numeric(df['Wholesale Price'], errors='coerce')

updated_rows = 0
for veg in vegetables:
    for dt in dates:
        stats = calculate_statistics(df, veg, pd.to_datetime(dt))
        stats = tuple(float(x) if x is not None else None for x in stats)
        update_query = """
        UPDATE VEG_DATA
        SET dma_30 = %s, dma_90 = %s, high_90 = %s, low_90 = %s, median_90 = %s, dma_90_prev = %s
        WHERE vegetable = %s AND date = %s
        """
        cursor.execute(update_query, (*stats, veg, dt))
        updated_rows += 1
        db.commit()

print(f"\n✅ Backfill complete. Total records updated: {updated_rows}")

cursor.close()
db.close()
print("🔚 All operations completed successfully.")

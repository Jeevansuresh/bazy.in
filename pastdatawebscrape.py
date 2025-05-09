import requests
from datetime import datetime, timedelta
import csv

def generate_date_range(start_date, end_date):
    current_date = start_date
    while current_date <= end_date:
        yield current_date
        current_date += timedelta(days=1)

start_date = datetime(2022, 1, 1)
end_date = datetime.today()

with open("vegetable_prices_all_days.csv", "w", newline="", encoding="utf-8") as csvfile:
    csvwriter = csv.writer(csvfile)
    header = ["Date", "Vegetable", "Wholesale Price", "Retail Min", "Retail Max", "Mall Min", "Mall Max", "Units"]
    csvwriter.writerow(header)

    for current_date in generate_date_range(start_date, end_date):
        formatted_date = current_date.strftime('%Y-%m-%d')
        url = "https://vegetablemarketprice.com/api/dataapi/market/chennai/daywisedata"
        params = {"date": formatted_date}
        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()

            for item in data['data']:
                vegetable = item["vegetablename"]

                # Skip non-English names (Tamil or others)
                if not vegetable.isascii():
                    continue

                wholesale_price = item["price"]

                retail_prices = item["retailprice"].split(" - ")
                retail_min = retail_prices[0] if len(retail_prices) > 1 else retail_prices[0]
                retail_max = retail_prices[1] if len(retail_prices) > 1 else retail_prices[0]

                mall_prices = item["shopingmallprice"].split(" - ")
                mall_min = mall_prices[0] if len(mall_prices) > 1 else mall_prices[0]
                mall_max = mall_prices[1] if len(mall_prices) > 1 else mall_prices[0]

                units = item["units"]

                data_row = [formatted_date, vegetable, wholesale_price, retail_min, retail_max, mall_min, mall_max, units]
                csvwriter.writerow(data_row)

        else:
            print(f"Failed to retrieve data for {formatted_date}. Status code:", response.status_code)

print("Filtered English-only vegetable data has been exported to 'vegetable_prices_all_days.csv'")

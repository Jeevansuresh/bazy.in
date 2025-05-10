import requests  # For sending HTTP requests and fetching web content
from bs4 import BeautifulSoup  # For parsing and navigating HTML
import mysql.connector  # For connecting to MySQL
import csv  # For writing the scraped data into a CSV file

# Define the URL of the webpage to scrape
url = "https://vegetablemarketprice.com/market/chennai/today"

# Send a GET request to the URL and store the response
response = requests.get(url)

# Function to clean the price data (remove ₹ symbol and commas)
def clean_price(value):
    return value.replace('₹', '').replace(',', '').strip()

# Connect to MySQL
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Skyno@1978",  # Change this to your MySQL password
    database="vegetables"  # Change this to your database name
)

cursor = db_connection.cursor()

# Create table if it doesn't exist (you can adjust the column types as needed)
create_table_query = """
CREATE TABLE IF NOT EXISTS VEG_DATA (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE,
    vegetable VARCHAR(255),
    wholesale_price DECIMAL(10, 2),
    retail_min DECIMAL(10, 2),
    retail_max DECIMAL(10, 2),
    mall_min DECIMAL(10, 2),
    mall_max DECIMAL(10, 2),
    units VARCHAR(50)
)
"""
cursor.execute(create_table_query)

# Check if the request was successful (status code 200 = OK)
if response.status_code == 200:
    # Parse the HTML content of the page using BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")

    # Find the first table on the page — this is where the price data is stored
    table = soup.find("table")

    # Proceed only if a table was found
    if table:
        # Find all rows (<tr>) in the table
        rows = table.find_all("tr")

        # Open (or create) a CSV file to write the data
        with open("vegetable_prices_today.csv", "w", newline="", encoding="utf-8") as csvfile:
            csvwriter = csv.writer(csvfile)  # Create a CSV writer object

            # Write the header row to the CSV file with the updated format
            header = ["Vegetable", "Wholesale Price", "Retail Min", "Retail Max", "Mall Min", "Mall Max", "Units"]
            csvwriter.writerow(header)

            # Iterate through all rows except the header (first row)
            for row in rows[1:]:
                # Find all columns (<td>) in the current row
                cols = row.find_all("td")

                # Extract and clean text from each column, skipping the first column
                vegetable = cols[1].text.strip().split('(')[0].strip()
                wholesale_price = clean_price(cols[2].text.strip())

                # Split Retail Price into Retail Min and Retail Max
                retail_prices = [clean_price(p) for p in cols[3].text.strip().split(" - ")]
                retail_min = retail_prices[0]
                retail_max = retail_prices[1] if len(retail_prices) > 1 else retail_prices[0]

                # Split Mall Price into Mall Min and Mall Max
                mall_prices = [clean_price(p) for p in cols[4].text.strip().split(" - ")]
                mall_min = mall_prices[0]
                mall_max = mall_prices[1] if len(mall_prices) > 1 else mall_prices[0]

                # Extract the Units column (assuming it's the last column in each row)
                units = cols[5].text.strip() if len(cols) > 5 else ""  # Check if there's a "Units" column

                # Write the extracted data to the CSV file
                data = [vegetable, wholesale_price, retail_min, retail_max, mall_min, mall_max, units]
                csvwriter.writerow(data)

                # Insert data into MySQL
                insert_query = """
                INSERT INTO VEG_DATA (date, vegetable, wholesale_price, retail_min, retail_max, mall_min, mall_max, units)
                VALUES (CURDATE(), %s, %s, %s, %s, %s, %s, %s)
                """
                try:
                    cursor.execute(insert_query, (
                        vegetable, wholesale_price, retail_min, retail_max, mall_min, mall_max, units
                    ))
                    db_connection.commit()  # Commit the changes to the database
                except mysql.connector.Error as err:
                    print(f"Failed to insert {vegetable}: {err}")
                    db_connection.rollback()

        print("Data has been exported to both 'vegetable_prices_today.csv' and MySQL.")
    else:
        print("No table found on the page.")
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")

# Close the database connection
cursor.close()
db_connection.close()

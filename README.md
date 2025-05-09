This project is designed to scrape vegetable price data from the Chennai Fresh Market website and load it into a MySQL database. The data includes details like wholesale prices, retail prices, and unit information for various vegetables, tracked daily. The program is structured to run initially to collect historical data and then continues to collect and insert daily data.

Project Structure:
pastdatawebscrape.py: The Python script responsible for web scraping vegetable price data from the Chennai Fresh Market website.

vegetable_prices_all_days.csv: The CSV file containing the scraped data for loading into the MySQL database.

pastdatawebscrapesql.py: The Python script that inserts the scraped data from the CSV file into the MySQL database (VEG_DATA table).

MySQL Database: The data is stored in the VEG_DATA table with the following columns:

date (YYYYMMDD format)

vegetable (English name only)

unit

wholesale_price

retail_min

retail_max

mall_min

mall_max

Key Features:
Scrapes historical data from 01/01/2022 to the current date.

Inserts the scraped data into a MySQL database for storage.

Runs the web scraping and insertion processes daily.

Cron job can be set up (on Linux) to automate the daily task at 3:30 PM IST.

How to Run:
Set up your MySQL database and create the VEG_DATA table.

Install the required Python libraries (requests, beautifulsoup4, mysql-connector).

Run pastdatawebscrape.py for the initial data scraping.

Use pastdatawebscrapesql.py to load the data into MySQL.

Set up a cron job or use a task scheduler (for Windows) to automate daily scraping.

Note: Cron job setup is not implemented as part of this project since the system is running on Windows, but instructions for setting it up on Ubuntu/Linux are provided.

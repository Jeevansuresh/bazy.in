Chennai Vegetable Market Price Scraper

This project scrapes daily vegetable price data from the Chennai Fresh Market and loads it into a MySQL database for analysis and record-keeping. It tracks wholesale and retail prices, mall prices, units, and vegetable names on a day-wise basis.

Features
Scrapes historical data from January 1, 2022, up to the current date.

Collects daily data and appends it to the database.

Organizes scraped data into CSV files (vegetable_prev_prices.csv and vegetable_prices_today.csv).

Loads structured data into a MySQL table (VEG_DATA).

Provides a summary of data received and missing dates (for historical fetches).

Cron job compatible for daily automation.

Project Structure
pastdatawebscrape.py – Scrapes historical data and loads it into the DB.

dailydatawebscrape.py – Scrapes the current day’s data and updates the DB daily.

Tech Stack
Python

MySQL

Requests

CSV

Phase 1 Completed
Historical backfill done

Daily scraper functional

Ready for deployment with scheduled automation

Phase 2 Completed
90_DMA (Days Moving Average): Tracks the 90-day and 30-day moving average of the wholesale price. Calculates by adding all the values of the past number of days and dividing by the number of days.

90_HIGH: Tracks the highest wholesale price in the rolling past 90 days.

90_LOW: Tracks the lowest wholesale price in the rolling past 90 days.

90_MEDIAN: Tracks the median wholesale price in the rolling past 90 days.

PREV_90_DMA: Compares the current year’s past 90 days (e.g., Feb 10th to May 7th, 2025) to the previous year’s past 90 days (e.g., Feb 10th to May 7th, 2024).

Updates calculated fields to the table (VEG_DATA) with: 90_DMA, 30_DMA, 90_HIGH, 90_LOW, 90_MEDIAN, PREV_90_DMA.

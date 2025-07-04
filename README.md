# Chennai Vegetable Market Data Tracker

A full-stack Python web application to scrape, store, analyze, and visualize daily vegetable prices from the Chennai market.

---

## 🌾 Project Overview

This project automates the scraping of daily vegetable prices from [vegetablemarketprice.com](https://vegetablemarketprice.com/market/chennai/today/), stores historical and live data in a MySQL database, performs rolling analytics, and displays insights via a web dashboard.

The project is divided into **four phases**:

---

## 📦 Phase 1: Data Scraping and Storage

### ✅ Tasks Completed

* Scrapes daily vegetable market data from the Chennai market page.
* Parses data fields:

  * `Calendar Date (YYYYMMDD)`
  * `Vegetable Name`
  * `Unit`
  * `Wholesale Price`
  * `Retail Min`
  * `Retail Max`
  * `Mall Min`
  * `Mall Max`
* Loops from **01/01/2022** to today to backfill historical data.
* Inserts data into a MySQL table `VEG_DATA`.
* Scheduled with a **cron job** to run daily at **3:30 PM IST / 6 PM EST**.

---

## 📈 Phase 2: Data Analysis & Rolling Metrics

### ✅ Tasks Completed

* Calculates rolling metrics:

  * **90-day Moving Average (90\_DMA)**
  * **30-day Moving Average (30\_DMA)**
  * **90-day High Price (90\_HIGH)**
  * **90-day Low Price (90\_LOW)**
  * **90-day Median Price (90\_MEDIAN)**
  * **Previous Year 90-day Average (PREV\_90\_DMA)**
* Updates these fields daily for each vegetable in the `VEG_DATA` table.
* Scheduled via a **cron job** to run after the scraper every day.

---

## 📊 Phase 3: Visualization Dashboard

### ✅ Tasks Completed

* Web-based interface with:

  * Dropdown menu to **select vegetables**
  * Line chart showing last 10 days of:

    * **Wholesale Price**
    * **90\_DMA**
    * **30\_DMA**
    * **90\_MEDIAN**
  * **Interactive and responsive** dashboard design

---

## ☂️ Phase 4: Weather Integration and Price Correlation

### ✅ Tasks Completed

* Scrapes daily weather data ( another Cronjob) of Chennai using the **Meteostat** Python module (observed METAR reports).
* Captures:

  * **Afternoon Temperature (°C)**
  * **Afternoon Rainfall (mm)**
* Stores weather data in a separate **MySQL table**
* Visualizes the correlation of:

  * **Price vs Temperature vs Rainfall** on a 10-day timeline
* Enables further study into how **climatic factors may influence vegetable pricing patterns**

---

## 🌐 Live Website

The website is currently live at: **[bazy.in](http://bazy.in)**

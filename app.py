from flask import Flask, render_template, request, jsonify
import mysql.connector
from datetime import datetime, timedelta

app = Flask(__name__)

DB_CONFIG = {
    "host": "localhost",
    "user": "jagi",
    "password": "Padjagi75$",
    "database": "vegetables"
}

@app.route('/')
def index():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT vegetable FROM VEG_DATA ORDER BY vegetable")
    vegetables = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return render_template('index.html', vegetables=vegetables)

@app.route('/get_data', methods=['GET'])
def get_data():
    veg = request.args.get('vegetable')
    if not veg:
        return jsonify({'error': 'No vegetable selected'}), 400

    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    end_date = datetime.today().date()
    start_date = end_date - timedelta(days=9)

    query = """
        SELECT date, wholesale_price, dma_90, dma_30, median_90
        FROM VEG_DATA
        WHERE vegetable = %s AND date BETWEEN %s AND %s
        ORDER BY date
    """
    cursor.execute(query, (veg, start_date, end_date))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    data = []
    for row in rows:
        data.append({
            'date': row[0].strftime('%Y-%m-%d'),
            'wholesale_price': float(row[1]) if row[1] is not None else None,
            'dma_90': float(row[2]) if row[2] is not None else None,
            'dma_30': float(row[3]) if row[3] is not None else None,
            'median_90': float(row[4]) if row[4] is not None else None
        })

    return jsonify(data)

@app.route('/get_weather_data', methods=['GET'])
def get_weather_data():
    veg = request.args.get('vegetable')
    if not veg:
        return jsonify({'error': 'No vegetable selected'}), 400

    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    end_date = datetime.today().date()
    start_date = end_date - timedelta(days=9)

    query = """
        SELECT 
            v.date,
            v.wholesale_price,
            w.an_temp AS afternoon_temp,
            w.an_rain AS afternoon_rain
        FROM
            vegetables.VEG_DATA v
        JOIN
            weather.CHENNAI_WEATHER w ON v.date = w.date
        WHERE
            v.vegetable = %s AND v.date BETWEEN %s AND %s
        ORDER BY
            v.date ASC
    """
    cursor.execute(query, (veg, start_date, end_date))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    data = []
    for row in rows:
        data.append({
            'date': row[0].strftime('%Y-%m-%d'),
            'wholesale_price': float(row[1]) if row[1] is not None else None,
            'afternoon_temp': float(row[2]) if row[2] is not None else None,
            'afternoon_rain': float(row[3]) if row[3] is not None else None
        })

    return jsonify(data)

@app.route('/get_weather_table', methods=['GET'])
def get_weather_table():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    end_date = datetime.today().date()
    start_date = end_date - timedelta(days=9)

    query = """
        SELECT date, morn_temp, morn_rain, an_temp, an_rain, eve_temp, eve_rain, night_temp, night_rain
        FROM weather.CHENNAI_WEATHER
        WHERE date BETWEEN %s AND %s
        ORDER BY date ASC
    """
    cursor.execute(query, (start_date, end_date))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    data = []
    for row in rows:
        data.append({
            'date': row[0].strftime('%Y-%m-%d'),
            'morn_temp': row[1], 'morn_rain': row[2],
            'an_temp': row[3], 'an_rain': row[4],
            'eve_temp': row[5], 'eve_rain': row[6],
            'night_temp': row[7], 'night_rain': row[8]
        })

    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

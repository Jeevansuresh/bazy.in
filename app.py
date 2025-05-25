from flask import Flask, render_template, request, jsonify
import mysql.connector
from datetime import datetime, timedelta

app = Flask(__name__)

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Skyno@1978",
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

if __name__ == '__main__':
    app.run(debug=True)

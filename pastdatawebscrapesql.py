import csv
import mysql.connector

db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Skyno@1978",
    database="vegetables"
)

cursor = db_connection.cursor()

delete_query = "DELETE FROM VEG_DATA"
cursor.execute(delete_query)
db_connection.commit()

csv_file_path = 'vegetable_prices_all_days.csv'

with open(csv_file_path, mode='r', encoding='utf-8') as file:
    csvreader = csv.reader(file)
    next(csvreader)

    insert_query = """
        INSERT INTO VEG_DATA (date, vegetable, wholesale_price, retail_min, retail_max, mall_min, mall_max, units)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    current_date = None

    for row in csvreader:
        try:
            date = row[0]
            vegetable = row[1].split('(')[0].strip()
            wholesale_price = row[2]
            retail_min = row[3]
            retail_max = row[4]
            mall_min = row[5]
            mall_max = row[6]
            units = row[7]

            if date != current_date:
                if current_date is not None:
                    db_connection.commit()
                    print(f"Data for {current_date} has been successfully inserted.")
                current_date = date

            data = (date, vegetable, wholesale_price, retail_min, retail_max, mall_min, mall_max, units)
            cursor.execute(insert_query, data)

        except Exception as e:
            print(f"Error processing row {row}: {e}")

    db_connection.commit()
    print(f"Data for {current_date} has been successfully inserted.")

print("CSV data has been successfully loaded into the VEG_DATA table.")

cursor.close()
db_connection.close()

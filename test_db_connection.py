import mysql.connector
from mysql.connector import Error

try:
    connection = mysql.connector.connect(
        host='localhost',
        user='jagi',
        password='Padjagi75$',
       
    )

    if connection.is_connected():
        print("✅ Successfully connected to the MySQL server.")
        print("MySQL Server version:", connection.get_server_info())

except Error as e:
    print("❌ Error while connecting to MySQL:", e)

finally:
    if 'connection' in locals() and connection.is_connected():
        connection.close()
        print("🔌 Connection closed.")

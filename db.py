from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
load_dotenv()  # Load environment variables from .env file

def connect_to_db():
    host = os.getenv("DB_HOST")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    database = os.getenv("DB_NAME")

    if not all([host, user, password, database]):
        print("Error: One or more environment variables are missing.")
        return None

    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        print("Database connection established.")
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to database: {err}")
        return None

@app.route("/")
def index():
    """Simple route to test database connection."""
    query = "SELECT 'Hello from MySQL on Vercel!' AS message"
    result = execute_query(query)
    if result:
        return jsonify({"message": result[0][0]})
    else:
        return jsonify({"error": "Failed to fetch data"}), 500

def execute_query(query, params=None):
    connection = connect_to_db()
    if connection is None:
        return None

    try:
        cursor = connection.cursor()
        cursor.execute(query, params or [])
        connection.commit()
        return cursor.fetchall()
    except Error as err:
        print(f"Error executing query: {err}")
        return None
    finally:
        if connection:
            connection.close()

if __name__ == "__main__":
    app.run(debug=True)

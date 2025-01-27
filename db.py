import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv  # If using a .env file (optional)

# Load environment variables from .env file (if you're using this option)
load_dotenv()

def connect_to_db():
    """Establish a connection to the MySQL database using environment variables."""
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

def execute_query(query, params=None):
    """Executes a database query with parameterized inputs to prevent SQL injection."""
    connection = connect_to_db()
    if connection is None:
        return None

    try:
        cursor = connection.cursor()
        cursor.execute(query, params or [])
        connection.commit()
        return cursor.fetchall()  # Returns the result of the query
    except Error as err:
        print(f"Error executing query: {err}")
    finally:
        if connection:
            connection.close()  # Always close the connection



import mysql.connector
import csv
import uuid
from mysql.connector import errorcode

def connect_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="your_mysql_username",
            password="your_mysql_password"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def create_database(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        print("Database ALX_prodev created or already exists")
    except mysql.connector.Error as err:
        print(f"Failed to create database: {err}")
    finally:
        cursor.close()

def connect_to_prodev():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="your_mysql_username",
            password="your_mysql_password",
            database="ALX_prodev"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Connection failed: {err}")
        return None

def create_table(connection):
    try:
        cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS user_data (
            user_id CHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL NOT NULL,
            INDEX(user_id)
        );
        """
        cursor.execute(create_table_query)
        print("Table user_data created successfully")
    except mysql.connector.Error as err:
        print(f"Error creating table: {err}")
    finally:
        cursor.close()

def insert_data(connection, csv_file):
    try:
        cursor = connection.cursor()
        with open(csv_file, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                user_id = row['user_id']
                name = row['name']
                email = row['email']
                age = row['age']
                
                cursor.execute("""
                    SELECT COUNT(*) FROM user_data WHERE user_id = %s
                """, (user_id,))
                exists = cursor.fetchone()[0]
                
                if not exists:
                    cursor.execute("""
                        INSERT INTO user_data (user_id, name, email, age)
                        VALUES (%s, %s, %s, %s)
                    """, (user_id, name, email, age))
        connection.commit()
        print("Data inserted successfully")
    except Exception as e:
        print(f"Error inserting data: {e}")
    finally:
        cursor.close()

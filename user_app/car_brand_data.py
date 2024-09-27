import secrets
import psycopg2
# import mysql.connector
from psycopg2 import Error

# Function to create a connection to the MySQL database
def create_connection(host_name, user_name, user_password, db_name):
    connection = None
    # try:
    connection = psycopg2.connect(
        host=host_name,
        user=user_name,
        password=user_password,
        database=db_name
    )
    print("Connection to MySQL DB successful")
    # except mysql.connector.Error as err:
    #     print(f"The error '{err}' occurred")
    # print('connection',connection)
    return connection

# Function to execute a single query
def execute_query(connection, query, params=None):
    cursor = connection.cursor()
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")
    finally:
        cursor.close()

# Function to execute multiple queries from a file
def execute_sql_file(connection, file_path):
    cursor = connection.cursor()
    try:
        with open(file_path, 'r') as file:
            sql_script = file.read()
            # lines = file.readlines()
            # print('sql_script', lines[2].split(',')[-3])
            
        for statement in sql_script.split(';'):
            if statement.strip():
                cursor.execute(statement)
        connection.commit()
        print("SQL file executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")
    finally:
        cursor.close()

# Function to generate a random token
# def generate_token():
#     return secrets.token_hex(16)

# Function to update rows with NULL remember_token
def update_null_tokens(connection):
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT id FROM car_trim WHERE remember_token IS NULL;")
        rows = cursor.fetchall()
        for row in rows:
            token = ""
            update_query = "UPDATE car_trim SET remember_token = %s WHERE id = %s"
            execute_query(connection, update_query, (token, row[0]))
        print(f"Updated {cursor.rowcount} rows with new tokens.")
    except Error as e:
        print(f"The error '{e}' occurred")
    finally:
        cursor.close()

# MySQL database connection details
host_name = "127.0.0.1"
user_name = "postgres"
user_password = "postgres"
db_name = "Revolution_Auto"

# Create the connection
connection = create_connection(host_name, user_name, user_password, db_name)

# Load and execute SQL file
sql_file_path = "/home/est/Downloads/cars.sql"
execute_sql_file(connection, sql_file_path)

# Update rows with NULL remember_token
# update_null_tokens(connection)

# Close the database connection
# if connection:
#     connection.close()
#     print("The connection is closed")

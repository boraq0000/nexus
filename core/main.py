# import psycopg2
# from dotenv import load_dotenv
# import os

# Utility module for database checks and environment loading.
# Load environment variables and connect to Supabase/PostgreSQL
# using Django settings.

# # Load environment variables
# load_dotenv()

# # Fetch variables
# DATABASE_URL = os.getenv("DATABASE_URL")

# try:
#     # Connect to the database
#     connection = psycopg2.connect(DATABASE_URL)
    
#     # Create a cursor to perform database operations
#     cursor = connection.cursor()
    
#     # Execute a simple query to get the database version
#     cursor.execute("SELECT version();")
#     db_version = cursor.fetchone()
    
#     print(" Successfully connected to Supabase!")
#     print(f" Database version: {db_version}")
    
#     # Close the connection
#     cursor.close()
#     connection.close()

# except Exception as e:
#     print(f" Connection failed! Error: {e}")
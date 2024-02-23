import pandas as pd

import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import config

class DatabaseManager:
    def __init__(self, host, port, user, password):
        self.host = host
        self.port = port
        self.user = user
        self.password = password

    def create_database(self, dbname):
        # Connect to PostgreSQL (template1 database) to create a new database
        connection = psycopg2.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            dbname='template1'
        )
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        # Create a cursor object to execute SQL commands
        cursor = connection.cursor()

        # Use the psycopg2.sql.SQL class to create the database for safer SQL string formatting
        create_db_query = sql.SQL("CREATE DATABASE  {}").format(
            sql.Identifier(dbname)
        )
        try:
            # Execute the SQL command to create the new database
            cursor.execute(create_db_query)
        except psycopg2.errors.DuplicateDatabase:
            pass


        create_db_query = sql.SQL(" CREATE SCHEMA fato"
        )
        try:
            # Execute the SQL command to create the new database
            cursor.execute(create_db_query)
        except psycopg2.errors.DuplicateSchema:
            pass

       
       
        # Use the psycopg2.sql.SQL class to create the table gastos for safer SQL string formatting
        create_db_query = sql.SQL("CREATE TABLE fato.gastos ("
            "  id SERIAL PRIMARY KEY,"
            " data DATE,"
            " ref VARCHAR(255),"
            " ref_fonte VARCHAR(255),"
            " valor FLOAT,"
            "categoria VARCHAR(255),"
            "data_inclusao Date,"
            "obs varchar(255)"
            ")" 
        )
        try:
            # Execute the SQL command to create the table gastos
           cursor.execute(create_db_query)
        except psycopg2.errors.DuplicateTable:
            pass

       

        # Use the psycopg2.sql.SQL class to create the table aportes for safer SQL string formatting
        create_db_query = sql.SQL("CREATE TABLE fato.gastos ("
            "  id SERIAL PRIMARY KEY,"
            " data DATE,"
            " pagante VARCHAR(255),"
            " valor FLOAT,"
            "data_inclusao Date"
            ")"       
        )
        try:
            # Execute the SQL command to create the new database
            cursor.execute(create_db_query)
        except psycopg2.errors.DuplicateTable:
            pass


        


        # Close the cursor and connection
        cursor.close()
        connection.close()

if __name__ == "__main__":
    # Replace these values with your PostgreSQL connection details
    db_manager = DatabaseManager(
        host=config.databaseSuperUser['Server'],
        port=config.databaseSuperUser['port'],
        user=config.databaseSuperUser['Username'],
        password=config.databaseSuperUser['password']
    )

    # Replace 'financas' with the desired database name
    db_manager.create_database('financas')

    print("Database 'financas' created successfully.")
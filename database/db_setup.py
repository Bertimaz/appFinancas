import pandas as pd
from tools import configure_logger
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import config
from db_connections import get_database_connection

class DatabaseManager:
    def __init__(self):
        pass

    def create_database(self, dbname):
        #Create a log
        logger=configure_logger('database\logs')        
        #Connect to DB
        logger.info('Connecting to DB')
        try:
            connection,cursor=get_database_connection()
            # Create a cursor object to execute SQL commands
            cursor = connection.cursor()
        except Exception as e:
            logger.critical(f'Erro ao conectar ao DB. Erro: {e}')
            quit()

        # Use the psycopg2.sql.SQL class to create the database for safer SQL string formatting
        create_db_query = sql.SQL("CREATE DATABASE  {}").format(
            sql.Identifier(dbname)
        )
        logger.info(f'Create DB: {dbname}')
        try:
            # Execute the SQL command to create the new database
            cursor.execute(create_db_query)
            logger.info(f'DB {dbname} Created')
        except psycopg2.errors.DuplicateDatabase:
            logger.info(f'database {dbname} already exists')
            print(f'database {dbname} already exists')
       
        ### CREATE Schem Fato
        create_db_query = sql.SQL(" CREATE SCHEMA fato"
        )
        logger.info('Creating Schema fato')
        try:
            # Execute the SQL command to create the new schem
            cursor.execute(create_db_query)
            logger.info('Schema fato Created')
            print('Schema fato Created')
        except psycopg2.errors.DuplicateSchema:
            print('Schema fato Already Exists')
            logger.info('Schema fato Already Exists')

              
        ### CREATE Schema DIM
        create_db_query = sql.SQL(" CREATE SCHEMA dim"
        )
        logger.info('Creating Schema Dim')
        try:
            # Execute the SQL command to create the new schem
            cursor.execute(create_db_query)
            logger.info('Schema dim Created')
            print('Schema dim Created')
        except psycopg2.errors.DuplicateSchema:
            print('Schema dim Already Exists')
            logger.info('Schema dim Already Exists')
    
        tables=['fato.gastos', 'fato.aportes','dim.usuarios','dim.contas', 'dim.contaUsuario']
        
        # Deleting tables
        logger.info(f'Deleting tables:{tables}')
        for table_name in tables:
            #Create SQL STRING
            create_db_query=sql.SQL(f'DROP TABLE {table_name} CASCADE;')
            try:
                #Execute Command
                cursor.execute(create_db_query)
                logger.info(f'Table {table_name} dropped')
            except Exception as e:
                logger.warning(f'Error on droping. {e}')

        # Create Table Usuarios 
        logger.info('Creating table dim.usuarios')
        create_db_query = sql.SQL("CREATE TABLE dim.usuarios ("
            "  id SERIAL PRIMARY KEY,"
            " nome varchar(255) NOT NULL,"
            " cpf int,"
            " senha VARCHAR(255) NOT NULL,"
            " email VARCHAR(255) NOT NULL"
            ")" 
        )  
        try:
            # Execute the SQL command to create the table dimusuarios
            cursor.execute(create_db_query)
            print('table dim.usuarios created')
            logger.info('table dim.usuarios created')
        except psycopg2.errors.DuplicateTable:
            print('table dim.usuario already exists')
            logger.info('table dim.usuario already exists')
        except Exception as e:
            logger.info(f'Unkown Error: {e}')


        #Criar table dim.contas
        logger.info('Creating table dim.contas')
        create_db_query = sql.SQL("CREATE TABLE dim.contas ("
            "id INT PRIMARY KEY,"
            " banco varchar(255) NOT NULL,"
            " agencia VARCHAR(255) NOT NULL,"
            " conta int NOT NULL"
            ")" 
        )
        try:
            # Execute the SQL command to create the table dim.contas
            cursor.execute(create_db_query)
            print('table dim.contas created')
            logger.info('table dim.contas created')
        except psycopg2.errors.DuplicateTable:
            print('table dim.contas already exists')
            logger.info('table dim.contas already exists')
        except Exception as e:
            logger.info(f'Unkown Error: {e}')

        # Create Table fato.gastos
        create_db_query = sql.SQL("CREATE TABLE fato.gastos ("
            "  id SERIAL PRIMARY KEY,"
            " data DATE,"
            " ref VARCHAR(255),"
            " ref_fonte VARCHAR(255),"
            " valor FLOAT,"
            "categoria VARCHAR(255),"
            "data_inclusao Date,"
            "conta INT REFERENCES dim.contas(id),"
            "obs varchar(255)"
            ")" 
        )
        logger.info('Creating table fato.gastos')
        try:
            # Execute the SQL command to create the table gastos
            cursor.execute(create_db_query)
            logger.info('table fato.gastos created')
            print('table fato.gastos created')
        except psycopg2.errors.DuplicateTable:
            print('table fato.gastos already exists')
            logger.info('table fato.gastos already exists')
            pass
        except Exception as e:
            logger.info(f'Unknown error: {e}')

        # Create table fato.aportes
        create_db_query = sql.SQL("CREATE TABLE fato.aportes ("
            "  id SERIAL PRIMARY KEY,"
            " data DATE,"
            " pagante_id INT REFERENCES dim.usuarios(id),"
            " valor FLOAT,"
            "data_inclusao Date"
            ")"       
        )
        logger.info('Creating table fato.aportes')
        try:
            # Execute the SQL command to create the table aportes
            cursor.execute(create_db_query)
            print('table fato.aportes created')
            logger.info('table fato.aportes created')
        except psycopg2.errors.DuplicateTable:
            print('table fato.aportes already exists')
            logger.info('table fato.aportes already exists')
        except Exception as e:
            logger.info(f'Unkown Error: {e}')   
            
        #Criar table dim.contaUsuario
        create_db_query = sql.SQL("CREATE TABLE dim.contaUsuario ("
            " id int PRIMARY KEY,"
            " usuarioId INT REFERENCES dim.usuarios(id),"
            " contaId INT REFERENCES dim.contas(id)"
            ")"
        )
        try:
            # Execute the SQL command to create the table contas
            cursor.execute(create_db_query)
            print('table dim.contas created')
            logger.info('table dim.contas created')
        except psycopg2.errors.DuplicateTable:
            print('table dim.contas already exists')
            logger.info('table dim.contas already exists')
        except Exception as e:
            logger.warning(f'Unkown Error: {e}')

        # Close the cursor and connection
        cursor.close()
        connection.close()
        
if __name__ == "__main__":
    # Replace these values with your PostgreSQL connection details
    db_manager = DatabaseManager()

    # Replace 'financas' with the desired database name
    db_manager.create_database('financas')

    print("Database 'financas' created successfully.")
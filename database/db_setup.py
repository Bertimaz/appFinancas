"""
Module that sets up the database
"""
from tools import configure_logger
import psycopg2
from psycopg2 import sql
from db_connections import get_database_connection



class DatabaseManager:
    def __init__(self):
        pass

    def create_database(self, dbname):
        #Create a log
        logger=configure_logger(r'database\logs')
        
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
        ### CREATE Schema Fato
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
    
        tables=['fato.transacao' ,'dim.usuario','dim.conta', 'dim.contaUsuario','dim.cartao','dim.cartaousuario']
        
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

        # Create Table usuario 
        logger.info('Creating table dim.usuario')
        create_db_query = sql.SQL("CREATE TABLE dim.usuario ("
            "  ID SERIAL PRIMARY KEY,"
            " nome varchar(255) NOT NULL,"
            " cpf int NOT NULL,"
            " senha VARCHAR(255) NOT NULL,"
            " email VARCHAR(255) NOT NULL"
            ")" 
        )  
        try:
            # Execute the SQL command to create the table dim.usuario
            cursor.execute(create_db_query)
            print('table dim.usuario created')
            logger.info('table dim.usuario created')
        except psycopg2.errors.DuplicateTable:
            print('table dim.usuario already exists')
            logger.info('table dim.usuario already exists')
        except Exception as e:
            logger.info(f'Unkown Error: {e}')


        #Criar table dim.conta
        logger.info('Creating table dim.conta')
        create_db_query = sql.SQL("CREATE TABLE dim.conta ("
            "ID INT PRIMARY KEY,"
            " banco varchar(255) NOT NULL,"   
            " agencia VARCHAR(255) NOT NULL,"
            " conta int NOT NULL"   # Preciso criptografar
            ")" 
        )
        try:
            # Execute the SQL command to create the table dim.contas
            cursor.execute(create_db_query)
            print('table dim.conta created')
            logger.info('table dim.conta created')
        except psycopg2.errors.DuplicateTable:
            print('table dim.contas already exists')
            logger.info('table dim.conta already exists')
        except Exception as e:
            logger.info(f'Unkown Error: {e}')

         #Criar table dim.cartao
        create_db_query = sql.SQL("CREATE TABLE dim.cartao ("
            " ID int PRIMARY KEY,"
            " usuario_ID INT REFERENCES dim.usuario(ID),"
            " credit_card_number INT NOT NULL,"  # Preciso criptografar
            " flag VARCHAR(255) NOT NULL,"
            "expiration_date DATE NOT NULL"
            ")"
        )
        try:
            # Execute the SQL command to create the table cartao
            cursor.execute(create_db_query)
            print('table dim.cartao created')
            logger.info('table dim.cartao created')
        except psycopg2.errors.DuplicateTable:
            print('table dim.cartao already exists')
            logger.info('table dim.cartao already exists')
        except Exception as e:
            logger.warning(f'Unkown Error: {e}')


        # Create Table fato.transacao
        create_db_query = sql.SQL("CREATE TABLE fato.transacao ("
            " ID SERIAL PRIMARY KEY,"
            " data DATE NOT NULL,"
            " ref_fonte VARCHAR(255) NOT NULL,"
            " ref VARCHAR(255),"
            " valor FLOAT NOT NULL,"
            " tipo_transacao VARCHAR (20) NOT NULL,"
            " categoria VARCHAR(255) NOT NULL,"
            " data_inclusao Date,"
            " conta_ID INT REFERENCES dim.conta(ID),"
            " credit_card_ID INT REFERENCES dim.cartao(ID),"
            " obs varchar(255)"
            ")" 
        )
        logger.info('Creating table fato.transacao')
        try:
            # Execute the SQL command to create the table fato.transacao
            cursor.execute(create_db_query)
            logger.info('table fato.transacao created')
            print('table fato.transacao created')
        except psycopg2.errors.DuplicateTable:
            print('table fato.transacao already exists')
            logger.info('table fato.transacao already exists')
            pass
        except Exception as e:
            logger.info(f'Unknown error: {e}')
 
        #Criar table dim.contaUsuario
        create_db_query = sql.SQL("CREATE TABLE dim.contaUsuario ("
            " ID int PRIMARY KEY,"
            " usuario_ID INT REFERENCES dim.usuario(ID),"
            " contaId INT REFERENCES dim.conta(ID)"
            ")"
        )
        logger.info('Creating table dim.contaUsuario')
        try:
            # Execute the SQL command to create the table dim.contaUsuario
            cursor.execute(create_db_query)
            print('table dim.contaUsuario created')
            logger.info('table dim.contaUsuario created')
        except psycopg2.errors.DuplicateTable:
            print('table dim.contaUsuario already exists')
            logger.info('table dim.contaUsuario already exists')
        except Exception as e:
            logger.warning(f'Unkown Error: {e}')

       
     #Criar table dim.cartaoUsuario
        create_db_query = sql.SQL("CREATE TABLE dim.cartaoUsuario ("
            " ID int PRIMARY KEY,"
            " usuario_ID INT REFERENCES dim.usuario(ID),"
            " cartao_ID INT REFERENCES dim.cartao(ID)"
            ")"
        )
        logger.info('Creating table dim.cartaoUsuario')
        try:
            # Execute the SQL command to create the table dim.cartaoUsuario
            cursor.execute(create_db_query)
            print('table dim.cartaoUsuario created')
            logger.info('table dim.cartaoUsuario created')
        except psycopg2.errors.DuplicateTable:
            print('table dim.cartaoUsuario already exists')
            logger.info('table dim.cartaoUsuario already exists')
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
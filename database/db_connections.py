"""
Module that manages db connections
"""

import config
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy import create_engine

def get_database_connection(existDB=False, engine='psycopg2'): 
    """
    Get conneection to the db
    Parameters:
    Engine: 'psycopg2' or 'sqlAlchemy
    Returns Tuple (conn,cursor) for psycopg and tupple (engine,connection) for sqlAlchemy
    """
    if engine=='psycopg2'
        if existDB:
            # Connect to PostgreSQL (template1 database) to create a new database
            connection = psycopg2.connect(
                host=config.databaseSuperUser['Server'],
                port=config.databaseSuperUser['port'],
                user=config.databaseSuperUser['Username'],
                password=config.databaseSuperUser['password'],
                database=config.databaseSuperUser['db_name']  
            )
        else:
            # Connect to PostgreSQL (template1 database) to create a new database
            connection = psycopg2.connect(
                host=config.databaseSuperUser['Server'],
                port=config.databaseSuperUser['port'],
                user=config.databaseSuperUser['Username'],
                password=config.databaseSuperUser['password']
            )
         #Get Cursor
        cursor = connection.cursor()
        #Returns  connection and Cursor 
        return connection,cursor


        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    elif engine=='sqlAlchemy':
        # Modify this line with your database URL
        db_url = 'postgresql://{}:{}@{}:{}/{}'.format(
            config.databaseSuperUser['Username'],
            config.databaseSuperUser['password'],
            config.databaseSuperUser['Server'],
            config.databaseSuperUser['port'],
            config.databaseSuperUser['db_name'] if existDB else ''
        )

        engine = create_engine(db_url)
        connection = engine.connect()
        # Return the engine and connection
        return engine, connection




   





def get_database_connection(existDB=False):
    """
    Get connection to the database
    Returns Tuple (engine, connection)
    """
    # Modify this line with your database URL
    db_url = 'postgresql://{}:{}@{}:{}/{}'.format(
        config.databaseSuperUser['Username'],
        config.databaseSuperUser['password'],
        config.databaseSuperUser['Server'],
        config.databaseSuperUser['port'],
        config.databaseSuperUser['db_name'] if existDB else ''
    )

    engine = create_engine(db_url)

    connection = engine.connect()
    # connection.

    # Return the engine and connection
    return engine, connection

"""
Module that manages db connections
"""

from database import config
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def get_database_connection(existDB=False): 
    """
    Get conneection to the db
    Returns Tuple (conn,cursor)
    """
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

    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    #Get Cursor
    cursor = connection.cursor()
    #Returns  connection and Cursor 
    return connection,cursor


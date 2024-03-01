import tools
import config
import db_connections
from psycopg2 import sql

def update_entry(connection_params, custom_condition, new_data):
    """
    Update an entry in the database based on a custom condition.

    Parameters:
    - custom_condition: Custom condition to identify the entry to be updated.
    - new_data: Dictionary containing the new data to be updated.
    
    # Example usage
    custom_condition = {"id": 1}  # Example custom condition
    new_data = {"name": "Updated Name", "age": 30}  # Example new data

    update_entry(custom_condition, new_data)
    """
    # Establish a connection to the database
    conn,cursor=db_connections.get_database_connection

    # Construct the SQL query based on the custom condition
    query = sql.SQL("UPDATE your_table SET {} WHERE {}").format(
    sql.SQL(', ').join(sql.SQL('{} = %s').format(sql.Identifier(col)) for col in new_data.keys()),
    sql.SQL(' AND ').join(sql.SQL('{} = %s').format(sql.Identifier(col)) for col in custom_condition.keys())
    )

    # Execute the query
    cursor.execute(query, list(new_data.values()) + list(custom_condition.values()))

    # Commit the changes
    connection.commit()

   
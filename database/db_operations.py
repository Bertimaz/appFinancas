import tools
import config
import db_connections
from psycopg2 import sql

def update_entry(table_name,custom_condition, new_data):
    """S
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
    conn,cursor=db_connections.get_database_connection()

    # Construct the SQL query based on the custom condition
    query = sql.SQL("UPDATE table {table} SET {set_columns} WHERE {conditions}").format(
    table=sql.Identifier(table_name),
    set_columns=sql.SQL(', ').join(sql.SQL('{} = %s').format(sql.Identifier(col)) for col in new_data.keys()),
    conditions=sql.SQL(' AND ').join(sql.SQL('{} = %s').format(sql.Identifier(col)) for col in custom_condition.keys())
)
    print(query)
    # Execute the query
    cursor.execute(query, list(new_data.values()) + list(custom_condition.values()))

    # Commit the changes
    conn.commit()
    conn.close()

def create_user(nome_usuario,nome,cpf,senha,email):
    """
    Create a new user

    Parameters:
    - nome_usuario: Nome de Usuário único
    - nome: nome  e sobrenome do usuario
    - cpf: no formato XXXXXXXXXXX, numero de 9 algarismos
    - senha
    - email

    
    # Example usage
    create_user('Albert Mazuz',00000000000,00000,'aaaa@aaaa.com.br')
    """
    #Validacoes
    if tools.validate_cpf(cpf) & tools.validate_email(email) & tools.validate_username(nome_usuario):
        #Conecntando
        conn,cursor=db_connections.get_database_connection(True)
        #Crypt password
        hashed_senha= tools.hash_password(senha)

        # Construct the SQL query based on the custom condition
        query = f"""INSERT INTO financas.dim.usuario  (nome_usuario,nome,cpf,senha,email)
        VALUES ('{nome_usuario}','{nome}', '{cpf}','{hashed_senha}','{email}')"""
        print(query)
        cursor.execute(query)
        conn.commit()
        conn.close()

def authenticate_user(username, password):
    # Here, you would retrieve the stored hashed password from your database based on the username
    stored_hashed_password = "..."  # Retrieve from database
    
    # Hash the provided password
    hashed_password = tools.hash_password(password)
    
    # Compare the hashes
    if hashed_password == stored_hashed_password:
        return True
    else:
        return False
    
def get_user_password(user_name): 
    """Função que recupera a senha haseada do usuário"""
    conn,c=db_connections.get_database_connection(existDB=True)
    c.execute(f"SELECT senha from financas.dim.usuario where nome_usuario='{user_name}'")
    return c.fetchone
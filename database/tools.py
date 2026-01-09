import logging
import os
from datetime import datetime
import re
import hashlib
import db_connections


def configure_logger(log_folder):
    # Create a logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    logging.basicConfig(level=logging.DEBUG)

    # Create the logs folder if it doesn't exist
    os.makedirs(log_folder, exist_ok=True)

    # Generate log file name based on current date and time
    current_datetime = datetime.now()
    log_file_name = f"log_{current_datetime.strftime('%Y%m%d_%H%M')}.log"
    log_file_path = os.path.join(log_folder, log_file_name)

    # Create a file handler and set the logging level
    file_handler = logging.FileHandler(log_file_path)
    file_handler.setLevel(logging.DEBUG)

    # Create a formatter and add it to the handler
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # Add the file handler to the logger
    logger.addHandler(file_handler)

    return logger

def validate_cpf(cpf):
  """
  This function validates if the input is a 9-digit number.

  Args:
      cpf numero de CPF como string.

  Raises:
      ValueError: 'cpf precisar ser um inteiro'
      ValueError: 'cpf precisar ter 11 digitos'
  """
  cpf=str(cpf)
  try:
    int(cpf)
  except:
    raise ValueError('cpf precisar ser um inteiro')
  
  if len(cpf) != 11:
    raise ValueError('cpf precisar ter 11 digitos')
  return True
  
def validate_username(user_name):
  """This functions validades a nome de usuario
  Args: 
  nome de usuário
  Return:
  True or False
  """
  conn,c=db_connections.get_database_connection(existDB=True)
  c.execute(f"Select nome_usuario from dim.usuario where nome_usuario='{user_name}'")
  # Get the number of entries
  num_entries = c.rowcount
  # Close the cursor and connection
  c.close()
  conn.close()
  if num_entries==0:
    raise ValueError('Nome de Usuário já existe')
  else:
    return True





def validate_email(email):
  """
  This function validates email format using regular expressions.

  Args:
      email: The email address to validate.

  Returns:
      True if the email format is valid, False otherwise.
  """
  pattern = r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$"
  if re.match(pattern, email):
    return True
  else:
    raise ValueError('Email Inválid')
  



def hash_password(password):
    # Convert the password to bytes
    password_bytes = password.encode('utf-8')
    
    # Hash the password using SHA-256 algorithm
    hashed_password = hashlib.sha256(password_bytes).hexdigest()
    
    return hashed_password
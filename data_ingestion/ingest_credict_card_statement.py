import sys
import pandas as pd
import tools
import logging

sys.path.append('../database')  # Add the 'database' directory to the Python path
sys.path.append('../../')   
from db_connections import get_database_connection


class Credit_Card_Statement_Pipeline:
    """Credit_Card_Statement_Pipeline: de ingestão de dados
     Attributes
    ----------
    type: str
        Define what type of extraction. Options: csv
    origin_path: str
        address of the extraction data
    load_path: str
        Address of the load table

    Methods
    extract():
        Extracts the information
    tranform()
    load()
    """



    def __init__(self) -> None:
        self.df=None
        self.cliente_id=None
        self.conta_id=None
        self.load_path=None
    def extract(self,origin_path):

        self.file_type=tools.get_file_type(origin_path)
        if self.file_type=='csv':
            self.df = pd.read_csv(origin_path)
        elif self.file_type in ('xls','xlsx'):
            self.df = pd.read_excel(origin_path)
        
        file_name=tools.get_fileName_from_filePath(origin_path)
        self.cliente_id=tools.get_userId_from_fileName(file_name)
        self.conta_id=tools.get_accountId_from_fileName(file_name)
        

    def transform(self):

        #Limpando linhas de saldo
        self.df = self.df[self.df['lançamento'] != "Controle de saldo"]

        #Renomeando as colunas
        self.df.rename(columns={'lançamento':'ref_fonte'},inplace=True)


        self.df['tipo_transacao']='cartão de crédito'
        self.df['conta_id']=self.conta_id
        self.df['usuario_id']=self.cliente_id

    def load(self,load_path='fato.transacao'):
        engine,connection=get_database_connection(existDB=True,engine='sqlAlchemy')
        n=self.df.to_sql(load_path, connection, if_exists='append', index=False)
        connection.commit()
        connection.close()
        tools.load_legado(self.df,'fatura')

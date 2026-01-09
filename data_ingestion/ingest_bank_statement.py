import sys
import pandas as pd
import tools
import logging
sys.path.append('../database')  # Add the 'database' directory to the Python path
sys.path.append('../../')   
from db_connections import get_database_connection

class Bank_Statement_Pipeline:
    """Pipeline de ingestão de dados
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
        self.df = pd.read_excel(origin_path)
        file_name=tools.get_fileName_from_filePath(origin_path)
        self.cliente_id=tools.get_userId_from_fileName(file_name)
        self.conta_id=tools.get_accountId_from_fileName(file_name)
        

    def transform(self):
        df = self.df.copy()
        # Encontrando primeira linha relevante
        first_line=-1
        #Finding first line
        for index,row in df.iterrows():
            if row.iloc[0]=='data':
                first_line=index
                break
        # Get relevante lines
        df=df.iloc[first_line:]
        # Promote first line to columns
        df.columns=df.iloc[0].to_list()
        df =df.iloc[1:]

        #Limpando linhas desnecessárias
        #Dropando lançamentos futuros
        df.reset_index(drop=True,inplace=True)
        index = df[df['data'] == 'lançamentos futuros'].index.item()
        df=df.iloc[0:index]

        #Dropand linhas de saldo
        df.dropna(subset=['valor (R$)'],inplace=True)
        df.reset_index(drop=True,inplace=True)


        #Dropando colunas Desnecessarias   saldos (R$) e ag./origem 
        df=df.drop(columns=['saldos (R$)','ag./origem'])

        df['tipo_transacao']='conta'
        df['conta_id']=self.conta_id
        df['usuario_id']=self.cliente_id
        
        #Renomeando colunas
        df.rename(columns={'data':'data','lançamento':'ref_fonte','valor (R$)':'valor','tipo_transacao':'tipo_transacao', 'conta_id':'conta_id','usuario_id':'usuario_id'},
                       inplace=True)
        
        self.df=df


    def load(self,load_path='fato.transacao'):
        engine,connection=get_database_connection(existDB=True,engine='sqlAlchemy')
        n=self.df.to_sql(load_path, connection, if_exists='append', index=False)
        connection.commit()
        connection.close()

        tools.load_legado(self.df,'extrato')


    

if __name__=='__main__':
    # origin_path='files\\extratos\\1_1_extrato_202512.xls'
    origin_path = 'file\\input\\1_1_extrato_202512.xlsx'
    pipeline=Bank_Statement_Pipeline()
    log = logging.getLogger(__name__)
    log.info('Extraindo Dados')
    pipeline.extract(origin_path)
    pipeline.df

    log.info('Carregando Dados')
    pipeline.load('financas.fato.transacao')
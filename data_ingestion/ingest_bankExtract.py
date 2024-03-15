import pandas as pd
import tools
class Pipeline:
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
        self.client_id=None
        self.account_id=None
    def extract(self,origin_path):
        self.data = pd.read_csv(origin_path)
        file_name=''
        self.client_id=tools.get_userId_from_fileName(file_name)
        self.account_id=tools.get_accountId_from_fileName(file_name)
        

    def transform(self):
        pass

    def load(self,load_path):
        pass

import logging

def main():
    log = logging.getLogger(__name__)
    log.info('Extraindo Dados')

    log.info('Transformando Dados')

    log('Carregando Dados')

if __name__=='__main__':
    main()
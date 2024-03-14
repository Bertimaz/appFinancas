# import pandas as pd
class Pipeline:
    """Pipeline de ingestão de dados
     Attributes
    ----------
    type: str
        Define what type of extraction. Options: csv
    extract_addres : str
        address of the extraction data
    load_address: str
        Address of the load table

    Methods
    extract():
        Extracts the information
    tranform()
    load()
    """
    def __init__(self) -> None:

        self.df=None
    def extract(origin_path):
        # file_path-''
        # data = pd.read_csv(file_path)
        pass

    def transform():
        pass

    def load(table_path):
        pass

import logging

def main():
    log = logging.getLogger(__name__)
    log.info('Extraindo Dados')

    log.info('Transformando Dados')

    log('Carregando Dados')

if __name__=='__main__':
    main()
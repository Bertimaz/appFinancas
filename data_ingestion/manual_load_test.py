from ingest_bank_statement import Bank_Statement_Pipeline
from ingest_credict_card_statement import Credit_Card_Statement_Pipeline
import tools

from pathlib import Path

# 1. Define the directory path
input_dir = Path("files/input")
history_dir = Path("files/historico")

# 2. Check if the directory exists to avoid errors
if input_dir.exists() and input_dir.is_dir():

    if not any(p.is_file() for p in input_dir.iterdir()):
        print("There are no files")
        
    # 3. Loop through files
    # Use .iterdir() for all files, or .glob("*.csv") for specific types
    for file_path in input_dir.iterdir():
        
        # Ensure we are only touching files (not subfolders)
        if file_path.is_file():
            print(f"Processing: {file_path.name}. {file_path}")
            file_name=tools.get_fileName_from_filePath(file_path=file_path.name)
            if 'extrato' in file_name.lower():
                Pipeline=Bank_Statement_Pipeline
            elif 'fatura' in file_name.lower():
                Pipeline=Credit_Card_Statement_Pipeline
            else:
                print('Nome do arquivo deve conter:' \
                'fatura para fatura da conta'\
                'extrato para extrato de cartão de crédito')

            destination = history_dir / file_path.name
            origin = input_dir / file_path.name
                
            pipeline=Pipeline()
            # Example: If you want to read them into pandas
            # quit()
            pipeline.extract(origin_path= str(origin))
            pipeline.transform()
            pipeline.load()


        
            print(f"Moving {file_path.name} to historico...")
            # Move the file
            tools.safe_rename(src=origin,dst=destination)

            print(f"Arquivo {file_name} Processado com sucesso")
            
else:
    print("The directory 'files/input' does not exist.")
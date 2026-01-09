import pickle

def get_userId_from_fileName(file_name):
    """
    Example usage:
    input_string = "1_2.xls"
    result = get_prefix_before_underscore(input_string)
    print(result)  # Output will be: 1
    """
    underscore_index=file_name.find('_')
    if underscore_index!=-1:
        return file_name[:underscore_index]
    else:
        raise ValueError('file name is in the wrong format. There is no underscore')

def get_accountId_from_fileName(file_name):
    """
    Expected format examples:
      "1_2_filename"
      "10_45_report"
    This extracts the value between the first and second underscores.
    """
    first_us = file_name.find('_')
    if first_us == -1:
        raise ValueError("File name format error: missing first underscore")

    # Find the next underscore after the first one
    second_us = file_name.find('_', first_us + 1)
    if second_us == -1:
        # If there's no second underscore, take the rest of the string
        return file_name[first_us + 1 :]

    return file_name[first_us + 1 : second_us]

    

def get_fileName_from_filePath(file_path):
    """
    Function that gets fileName from filePath
    Example
    filePath='folder/folder/dados.jpg'
    result=get_fileName_from_filePath(filePath)
    print(result) # Output will be 'dados'
    """
    # Find the index of the last occurrence of '/'
    last_slash_index = file_path.rfind('\\')
    
    # If '/' exists, return the substring after it, otherwise return the whole string
    if last_slash_index != -1:
        return file_path[last_slash_index + 1:]
    else:
        return file_path
    

def get_file_type(file_name):
    dot_index = file_name.rfind('.')
    if dot_index == -1:
        raise ValueError("File name format error: no file extension found.")
    return file_name[dot_index + 1:]

import unicodedata

def remove_accents(text):
    # Normalize the text into decomposed form
    normalized = unicodedata.normalize('NFD', text)
    # Keep only characters that are NOT accent marks ("Mn" = Mark, non-spacing)
    return ''.join(c for c in normalized if unicodedata.category(c) != 'Mn')

def categorize_transaction(reference:str):
    category = categorize_transaction_key_words(reference=reference)
    if category=='Não Categorizado':
        category=categorize_transaction_ml(reference=reference)

    return category

def categorize_transaction_key_words(reference:str):
    CATEGORY_RULES = {
    "Aporte":['TRANSF JESSICA','PAGTO SALARIO','TRANSF ALBERT'],
    "Saúde": ['farmácia','droga','saúde','panvel'],
    "Carro" :[],
    "Casa":[],
    "Contas Fixas":['comgas','claro','eletropaulo','enel','BOLETO SANDRA REGINA DE ANDRADE'],
    "Cultura":[],
    "Jiló":['Nutroplus','Petz',"Animau",'swift'],
    "Lazer":[],
    "Mercado":['hortifruti','Peg Pese'],
    "Restaurante":[],
    "Transporte":['Conectc','estacionamento','Porto Seguro','posto','estapar'],
    "Turismo":[],
    "Educação":["ENSINO"],
    "Variados":[],
    "Investimento":['cdb','APLICACAO COFRINHOS'],
    "Rendimento":['REND']
}
    ref = reference.lower()
    ref=remove_accents(ref)
    
    for category, keywords in CATEGORY_RULES.items():
        for kw in keywords:
            if kw.lower() in ref:
                return category
    
    return "Não Categorizado"

import numpy as np
def categorize_transaction_ml(reference:str):
    # Não Categorizado
    THRESHOLD = 0.6   # adjust as you like
    with open('models/transaction_classifier_1.pkl', 'rb') as f:
        model = pickle.load(f)
    with open('models/transaction_vectorizer_1.pkl', 'rb') as f:
        vectorizer = pickle.load(f)

    with open('models/transaction_label_encoder_1.pkl', 'rb') as f:
        le = pickle.load(f)


        # transform reference into model input
    X = vectorizer.transform([reference])

    # prediction
    pred = model.predict(X)[0]

    decoded_label = le.inverse_transform([pred])[0] 

    # probabilities
    probs = model.predict_proba(X)[0]
    certainty = np.max(probs)

    # threshold logic
    if certainty < THRESHOLD:
        return "Não Categorizado"

    return  decoded_label

def load_legado(df,tipo=""):
    df=df.copy()
    df['ref']=''
    df['Obs']=''

    df["Fonte"] = df["tipo_transacao"].apply(
        lambda x: "Débito" if x == "conta" else "Crédito"
    )
    df.rename(columns={'ref_fonte':'Ref Original'},inplace=True)

    df = df[~df['Ref Original'].str.contains('PERS BLACK 3600-8022', na=False, regex=False)]
    df["Categoria"] = df["Ref Original"].apply(lambda x: categorize_transaction(x))
    df=df[['data','Ref Original','ref','valor','Categoria','Fonte','Obs']]

    df.to_excel(f"{tipo}.xlsx",index=False)

    
    return df


from pathlib import Path

def safe_rename(src: Path, dst: Path):
    """
    Renomeia/move um arquivo adicionando (1), (2), (3)... caso o destino já exista.
    """
    new_dst = dst
    counter = 1

    # Divide em nome + extensão
    stem = dst.stem
    suffix = dst.suffix
    parent = dst.parent

    # Enquanto existir, gera outro nome
    while new_dst.exists():
        new_dst = parent / f"{stem} ({counter}){suffix}"
        counter += 1

    src.rename(new_dst)
    return new_dst


if __name__=='__main__':
    # print(get_fileName_from_filePath('data_ingestion\\files\\extratos\\1_1.xlsx'))
    print(categorize_transaction('PIX TRANSF JESSICA04/12'))



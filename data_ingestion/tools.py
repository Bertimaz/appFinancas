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
    Example usage:
    input_string = "1_2.xls"
    result = get_accountId_from_fileName(input_string)
    print(result)  # Output will be: 2
    """
    underscore_index=file_name.find('_')
    dot_index=file_name.find('.')
    if underscore_index!=-1 and dot_index!=-1:
        return file_name[underscore_index+1:dot_index]
    elif underscore_index==-1:
        raise ValueError('file name is in the wrong format. There is no underscore')
    elif underscore_index==-1:
        raise ValueError('file name is in the wrong format. There is no dot')
    

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

print(get_fileName_from_filePath('data_ingestion\\files\\extratos\\1_1.xlsx'))
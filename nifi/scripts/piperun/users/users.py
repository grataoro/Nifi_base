# script que puxa os dados de usuários do piperun e salva na tabela de usuarios dp redshift
try:
    import os
    import sys
    import pandas as pd

    # acessa o diretorio anteriro com a biblioteca do piperun  
    dir_path = os.path.dirname(os.path.realpath(__file__))
    path = os.path.normpath(dir_path + '/..') 
    sys.path.append(path)

    from pipe_lib import piperun

    # acessa os diretorios de bibliotecas do nifi 
    path = os.path.normpath(dir_path + '/../../..') 
    sys.path.append(path)

    import libs.logs_lib as log
    from libs.pgsql import pgsql_class as pg
    
    # Retorna o nome do diretorio 
    dir_name = os.path.basename(__file__)

    # url para usuarios ativos 
    url1 = "https://api.pipe.run/v1/users?show=200&page={}"

    response1 = piperun().get(url1) 

    # url para usuarios inativos 
    url = "https://api.pipe.run/v1/users?active=0&show=200&page={}"
    response = response1 + piperun().get(url) 
    coluns = ['id','name','email','active']
    table_name = 'users'

    #trata os dados para o formato aceito pelo redshift 
    df = pd.DataFrame(response)[coluns]
    records = df.to_records(index=False).tolist()

    pg("polichat").exec_pgsql("delete from piperun.{}".format(table_name)) # exclui todos os dados da tabela de usuarios 
    pg("polichat").to_pgsql(records, "piperun.{}".format(table_name)) # salva os dados na tabela de usuarios da poli 

    print(log.logs().susses(dir_name)) # retorna um json de logs

except Exception as e:

    print(log.logs().exception(dir_name,e)) # retorna um json de logs 

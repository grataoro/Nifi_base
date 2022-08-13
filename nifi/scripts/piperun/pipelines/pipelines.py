# scripts para migrar dados dos funis do piperun para o redshift 
import os
import sys

dir_path = os.path.dirname(os.path.realpath(__file__))
path = os.path.normpath(dir_path + '/..') 
sys.path.append(path)

from pipe_lib import tabelas

dir_name = os.path.basename(__file__)

url = "https://api.pipe.run/v1/pipelines?show=200&page={}"
coluns = ['id','funnel_type','funnel_type_name','name']
table_name = 'pipelines'

print(tabelas.main(url,coluns,table_name,dir_name))


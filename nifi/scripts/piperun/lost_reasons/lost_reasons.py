import os
import sys

dir_path = os.path.dirname(os.path.realpath(__file__))
path = os.path.normpath(dir_path + '/..') 
sys.path.append(path)

from pipe_lib import tabelas

dir_name = os.path.basename(__file__)

url = "https://api.pipe.run/v1/lostReasons?show=200&page={}"
coluns = ['id','name']
table_name = 'lost_reasons'

print(tabelas.main(url,coluns,table_name,dir_name))
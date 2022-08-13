
import os
import sys

dir_path = os.path.dirname(os.path.realpath(__file__))
path = os.path.normpath(dir_path + '/..') 
sys.path.append(path)

from pipe_lib import customFields

dir_name = os.path.basename(__file__)

table = 'piperun.company_customfields'
id_column = 'company_id'

url_cr = "https://api.pipe.run/v1/companies?created_at_start={}&with=customFields&show=200&page={}"

customFields().main(url_cr,dir_name,table,id_column) 
url_up = "https://api.pipe.run/v1/companies?updated_at_start={} 00:00:00&with=customFields&show=200&page={}"

print(customFields().main(url_up,dir_name,table,id_column))
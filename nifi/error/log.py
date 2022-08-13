import os
import sys
import json


inn = sys.stdin.read()

dir_path = os.path.dirname(os.path.realpath(__file__))
path = os.path.normpath(dir_path + '/..') 
sys.path.append(path)


from libs.pgsql import pgsql_class as pg

response = json.loads(inn)


location = response['location']
error    = response['response']
date     = response['time']   


records  = [(location,error,date)]

print(pg('polichat').to_pgsql(records,'poli.log_nifi (location,error,date)'))
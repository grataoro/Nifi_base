import os
import sys
import json

dir_path = os.path.dirname(os.path.realpath(__file__))
path = os.path.normpath(dir_path + '/../../..') 
sys.path.append(path)

from libs.pgsql import pgsql_class as pg

input = json.loads(sys.stdin.read())


status      = input["status"]
response    = input['response']
origin      = input['origin']   
end_time    = input['end_time'] 

records  = [(status,response,origin,end_time)]

print(pg('polichat').to_pgsql(records,'public.logs_webhook (status,response,origin,end_time)'))
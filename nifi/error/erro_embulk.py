import sys 
import json
from datetime import datetime

stdin = sys.stdin.read()
if 'Next config diff' in stdin:
	print(json.dumps({"status":"1", "response":'foi'}))
else:
	print(json.dumps({"status":"0", "location": "teste" , "response":'erro embulk', "time": datetime.today().strftime('%Y-%m-%d %H:%M:%S')})) 	

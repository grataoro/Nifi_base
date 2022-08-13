import json 
from datetime import datetime,timedelta

class logs:

    def __init__(self):
        self.end_time = (datetime.now() + timedelta(hours=-3)).strftime(format= "%Y-%m-%d %H:%M:%S")
 
    def susses(self,dir_name):
        return  json.dumps({"status":1, "response":"Success","origin":dir_name, "end_time":self.end_time})

    def exception(self,dir_name,e): 
        return json.dumps({"status":0, "response": str(e), "origin":dir_name,"end_time":self.end_time})
   
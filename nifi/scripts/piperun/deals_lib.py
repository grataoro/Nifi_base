import os
import re
import sys
import json
import traceback
import numpy as np
import pandas as pd

from unidecode import unidecode
from datetime import datetime, timedelta


from pipe_api_lib import pipeApi 


dir_path = os.path.dirname(os.path.realpath(__file__))
path = os.path.normpath(dir_path + '/../..') 
sys.path.append(path)

from libs.pgsql import pgsql_class as pg



class deals:

    extractedData   : list = []
    transformedData : list = []


    def main(self,dealUrl : str, dirName : str, up: str = None)->json:
        try:
            self.extract(dealUrl)
            self.transform(self.extractedData)
            self.load(up)

            end_time   = (datetime.now() + timedelta(hours=-3)).strftime(format= "%Y-%m-%d %H:%M:%S")
            return json.dumps({"status":1, "response":"Success","origin":dirName, "end_time":end_time})
        except:
            end_time   = (datetime.now() + timedelta(hours=-3)).strftime(format= "%Y-%m-%d %H:%M:%S")
            return json.dumps({"status":0, "response": str(traceback.format_exc()), "origin":dirName,"end_time":end_time})  


    def load(self,up:str) -> None:

        n_rows = 50000
        tableNAmeWithSchema : str = 'public.deals'
        tableWithColumns    : str = "public.deals (id, company_id, pipeline_id, stage_id, origin_id, owner_id, user_id, lost_reason_id, title, status_id, situation, mrr, value, temparatura, created_at, closed_at, updated_at)"
        


        con = pg().con
        cursor = con.cursor() 

        if up:
            idsFromTransformedData = pipeApi.ids(self.transformedData)
            cursor.execute(f"delete from {tableNAmeWithSchema} where id in {idsFromTransformedData}")

        else:
            day = (datetime.now() + timedelta(days=-2,hours=-3)).strftime('%Y-%m-%d') + ' 23:59:59'
            cursor.execute(f"delete from {tableNAmeWithSchema} where created_at >'{day}'")

       
        for i in range(0,len(self.transformedData),n_rows):

            record = self.transformedData[i:i+n_rows]

            records_list_template = ','.join(['%s'] * len(record))

            insert_query = 'insert into {} values {}'.format(tableWithColumns,records_list_template)

            if record:
                cursor.execute(insert_query, record)

        con.commit()

        cursor.close()
        con.close()
    


    def transform(self,dealsFromApi : list) -> None:
        lista = []

        for deal in dealsFromApi:

            if deal['deleted'] == 1:
                situation = 1
            elif  deal['freezed'] == 1:
                situation = 2
            else:
                situation = 0       

            if deal['users']:
                id_user = deal['users'][0]['id']
            else:
                id_user = None 

            dic = {

                'id'             : deal['id'],
                'id_comapny'     : deal['company_id'],
                'id_pipeline'    : deal['pipeline_id'],
                'id_stage'       : deal['stage_id'],
                'id_origin'      : deal['origin_id'], 
                'id_owner'       : deal['owner_id'],
                'id_user'        : id_user,
                'id_lost_reason' : deal['lost_reason_id'],
                'title'          : self.validation(deal['title']),
                'status'         : deal['status'],
                'situation'      : situation,
                'value_mrr'      : deal['value_mrr'],
                'value'          : deal['value'],
                'temperature'    : deal['temperature'],
                'created_at'     : deal['created_at'],
                'closed_at'      : deal['closed_at'],
                'updated_at'     : deal['updated_at']
            }    

            lista.append(dic)

        dfDeals = pd.DataFrame(lista)
        dfDeals.replace({np.nan: None},inplace=True)

        self.transformedData = dfDeals.to_records(index=False).tolist()   
    



    def extract(self,dealUrl:str) -> None:
        day = (datetime.now() + timedelta(days=-1,hours=-3)).strftime('%Y-%m-%d')
        self.extractedData = pipeApi().get(dealUrl,day)


    def validation(self,string : str) -> str:
        regexRule = re.compile(r"[^ a-zA-Z0-9@\-+=/()[\]*:!$%&.]")
        string = unidecode(string)
        return pipeApi.str_validation(regexRule.sub(r'',string).strip(),256)    

        
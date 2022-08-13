import os 
import sys

import json
import traceback
from datetime import datetime, timedelta

from soupsieve import select



dir_path = os.path.dirname(os.path.realpath(__file__))
path = os.path.normpath(dir_path + '/../..') 
sys.path.append(path)

from libs.mysql import mysql_class as my 
from libs.pgsql import pgsql_class as pg
from libs.sql_to_records import sqlTransform


class migrate:

    extractedDataCreated : list = []
    trasnformedData      : list = []

    def __init__(self,selectQuery : str) -> None:
        self.selectQuery : str = selectQuery
        

    def main(self, tableWithColumns : str, dirName : str ) -> json:
        try:

            self.extract_daly(self.selectQuery)
            
            self.transform()

            self.load(tableWithColumns)

            end_time   = (datetime.now() + timedelta(hours=-3)).strftime(format= "%Y-%m-%d %H:%M:%S")
            return json.dumps({"status":1, "response":"Success","origin":dirName, "end_time":end_time})
        except:
            end_time   = (datetime.now() + timedelta(hours=-3)).strftime(format= "%Y-%m-%d %H:%M:%S")
            return json.dumps({"status":0, "response": str(traceback.format_exc()), "origin":dirName,"end_time":end_time})
 



    def load(self,tableWithColumns : str) -> None:

        n_rows = 50000

        con = pg().con
        cursor = con.cursor() 
        

        records_list_template = ','.join(['%s'] * len(self.trasnformedData))

        insert_query = 'insert into {} values {}'.format(tableWithColumns,records_list_template)


        for i in range(0,len(self.trasnformedData),n_rows):

            record = self.trasnformedData[i:i+n_rows]

            records_list_template = ','.join(['%s'] * len(record))

            insert_query = 'insert into {} values {}'.format(tableWithColumns,records_list_template)

            if record:
                cursor.execute(insert_query, record)

        con.commit()

        cursor.close()
        con.close()



    def transform(self) -> None:
        self.trasnformedData = sqlTransform(self.extractedDataCreated).records() 
        

    def extract_daly(self,selectQuery:str)-> None:

        initTimestamp : datetime  = (datetime.now() + timedelta(days=-2,hours=-3)).date().strftime(format = "%Y-%m-%d") + ' 23:59:59'
        endTimestamp  : datetime  = (datetime.now() + timedelta(days=0,hours=-3)).date().strftime(format = "%Y-%m-%d") + ' 00:00:00'
        

        selectCreated = f"""

            {selectQuery}
            WHERE created_at > '{initTimestamp}'
            AND   created_at < '{endTimestamp}'
            
            """


        self.extractedDataCreated = my('polichat').from_mysql(selectCreated)

        
       

if __name__ == "__main__":

    select_messages = """
    select id, created_at, customer_id, channel_id, user_id, contact_id, message_type, message_dir, chat_id, in_reply_to, message_cuid
    from messages
    """
    
    tableWithColumns = "public.messages (id, created_at, customer_id, channel_id, user_id, contact_id, message_type, message_dir, chat_id, in_reply_to, message_cuid)"
    
    main = migrate(select_messages).main(tableWithColumns,'messages')

    print(main)       
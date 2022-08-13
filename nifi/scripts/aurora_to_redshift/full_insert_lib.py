import os 
import sys

import json
import traceback
from datetime import datetime, timedelta


dir_path = os.path.dirname(os.path.realpath(__file__))
path = os.path.normpath(dir_path + '/../..') 
sys.path.append(path)

from libs.mysql import mysql_class as my
from libs.pgsql import pgsql_class as pg
from libs.sql_to_records import sqlTransform


class fullInsert:

    extractedData : list = []
    trasnformedData : list = []

    def __init__(self,selectQuery : str) -> None:
        self.selectQuery : str = selectQuery
        

    def main(self,tableWithColumns : str,tableNAmeWithSchema : str, dirName : str):
        try:
            self.extract(self.selectQuery)
            self.transform()
            self.load(tableWithColumns, tableNAmeWithSchema)

            end_time   = (datetime.now() + timedelta(hours=-3)).strftime(format= "%Y-%m-%d %H:%M:%S")
            return json.dumps({"status":1, "response":"Success","origin":dirName, "end_time":end_time})
        except:
            end_time   = (datetime.now() + timedelta(hours=-3)).strftime(format= "%Y-%m-%d %H:%M:%S")
            return json.dumps({"status":0, "response": str(traceback.format_exc()), "origin":dirName,"end_time":end_time})
 



    def load(self,tableWithColumns : str,tableNAmeWithSchema : str) -> None:

        n_rows = 50000

        con = pg().con
        cursor = con.cursor() 

        
        cursor.execute("DELETE FROM {}".format(tableNAmeWithSchema))

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

        pass

    def transform(self) -> None:
        self.trasnformedData = sqlTransform(self.extractedData).records() 
    

    def extract(self,selectQuery : str) -> None:
        self.extractedData = my("polichat").from_mysql(selectQuery)
        


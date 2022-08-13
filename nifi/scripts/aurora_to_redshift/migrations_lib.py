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


class migrate:

    extractedDataCreated : list = []
    extractedDataUpdated : list = [] 
    extractedData        : list = []
    trasnformedData      : list = []

    def __init__(self,selectQuery : str) -> None:
        self.selectQuery : str = selectQuery
        

    def main(self,tableWithColumns : str,tableNAmeWithSchema : str, dirName : str, daly = None ) -> json:
        try:

            if daly:
                self.extract_daly(self.selectQuery)
            else:
                self.extract_full(self.selectQuery)


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

        if self.extractedDataUpdated:
            updated_data_id = tuple([ids[0] for ids in self.extractedDataUpdated])
            cursor.execute(f'delete from {tableNAmeWithSchema} where id in {updated_data_id}')
        

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
        self.trasnformedData = sqlTransform(self.extractedData).records() 
    

    def extract_full(self,selectQuery : str) -> None:
        self.extractedData = my("polichat").from_mysql(selectQuery)
        

    def extract_daly(self,selectQuery:str)-> None:

        initTimestamp : datetime  = (datetime.now() + timedelta(days=-2,hours=-3)).date().strftime(format = "%Y-%m-%d") + ' 23:59:59'
        endTimestamp  : datetime  = (datetime.now() + timedelta(days=0,hours=-3)).date().strftime(format = "%Y-%m-%d") + ' 00:00:00'
        createdEnd    : datetime  = (datetime.now() + timedelta(days=-1,hours=-3)).date().strftime(format = "%Y-%m-%d") + ' 00:00:00' 

        selectCreated = f"""

            {selectQuery}
            WHERE created_at > '{initTimestamp}'
            AND   created_at < '{endTimestamp}'
            

        """
        selectUpdated = f"""

            {selectQuery}
            WHERE updated_at > '{initTimestamp}' 
            AND   updated_at < '{endTimestamp}'
            AND   created_at < '{createdEnd}'

        """
        self.extractedDataCreated = my('polichat').from_mysql(selectCreated)
        self.extractedDataUpdated = my('polichat').from_mysql(selectUpdated)
        self.extractedData = self.extractedDataCreated + self.extractedDataUpdated
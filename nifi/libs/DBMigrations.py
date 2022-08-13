import os 
import sys
import json
import traceback
import numpy as np
import pandas as pd

from datetime import datetime, timedelta

dir_path = os.path.dirname(os.path.realpath(__file__))
path = os.path.normpath(dir_path + '/..') 
sys.path.append(path)

from libs.mysql import mysql_class as my
from libs.pgsql import pgsql_class as pg 


class sql_to_records:

    def records(data):
        df = pd.DataFrame(data)

        timestamp = list(df.dtypes[df.dtypes == 'datetime64[ns]'].index)
        for i in timestamp:
            df[i] = df[i].astype(str)

        df.replace({'NaT': None}, inplace=True)
        df.replace({np.nan: None}, inplace=True)
        return df.to_records(index = False).tolist()


class all_aurora_to_redshift:

    def deleteAllDataFromTable(tableNameWithSchema):
        return pg().exec_pgsql("DELETE FROM {}".format(tableNameWithSchema))
        

    def execSelectQuery(selectQuery):
        return my("polichat").from_mysql(selectQuery)


    def insertRecordsInTable(records,tableName):
        return pg().to_pgsql(records,tableName)



    def migration(selectQuery,RedshiftTableNameWithColumns,RedshifttableName, dirName):
        try:

            n_rows = 50000

            data    = all_aurora_to_redshift.execSelectQuery(selectQuery)
            records = sql_to_records.records(data)

            print(len(records))
            #all_aurora_to_redshift.deleteAllDataFromTable(RedshifttableName)

            # for i in range(0,len(records),n_rows):
            #     record = records[i:i+n_rows]
            #     all_aurora_to_redshift.insertRecordsInTable(record,RedshiftTableNameWithColumns)

            # end_time   = (datetime.now() + timedelta(hours=-3)).strftime(format= "%Y-%m-%d %H:%M:%S")
            
            return "foi" #json.dumps({"status":1, "response":"Success","origin":dirName, "end_time":end_time})

        except:
            #end_time   = (datetime.now() + timedelta(hours=-3)).strftime(format= "%Y-%m-%d %H:%M:%S")
            return "não foi" #json.dumps({"status":0, "response": str(traceback.format_exc()), "origin":dirName,"end_time":end_time})
 


class daly_aurora_to_redshift:
    
    def __init__(self):
        self.created_cr_init = (datetime.now() + timedelta(days=-2,hours=-3)).date().strftime(format = "%Y-%m-%d") + ' 23:59:59'
        self.created_cr_fim  = (datetime.now() + timedelta(days=0,hours=-3)).date().strftime(format = "%Y-%m-%d") + ' 00:00:00'

        self.updated_up_init = (datetime.now() + timedelta(days=-2,hours=-3)).date().strftime(format = "%Y-%m-%d") + ' 23:59:59'
        self.updated_up_fim  = (datetime.now() + timedelta(days=0,hours=-3)).date().strftime(format = "%Y-%m-%d") + ' 00:00:00'
        self.created_up_fim  = (datetime.now() + timedelta(days=-1,hours=-3)).date().strftime(format = "%Y-%m-%d") + ' 00:00:00' 


    def created(self,select,insert):

        select_created = """
            {}
            WHERE created_at > '{}'
            AND   created_at < '{}' 
            """.format(select,self.created_cr_init,self.created_cr_fim)

        created_data = my("polichat").from_mysql(select_created)

        for i in range(0,len(created_data),50000):
            records = sql_to_records.records(created_data[i:i+50000])
            pg('polichat').to_pgsql(records,insert)

        return 'foi'

    def updated(self,select,insert,table):

        select_updated = """    
            {}
            WHERE updated_at > '{}' 
            AND   updated_at < '{}'
            AND   created_at < '{}' 
            """.format(select,self.updated_up_init,self.updated_up_fim,self.created_cr_init)

        updated_data = my("polichat").from_mysql(select_updated)

        updated_data_id = tuple([ids[0] for ids in updated_data])
        pg('polichat').exec_pgsql('delete from {} where id in {}'.format(table,updated_data_id))

        for i in range(0,len(updated_data),50000):
            records = sql_to_records.records(updated_data[i:i+50000])
            pg('polichat').to_pgsql(records,insert) 

        return 'foi'

    def migration(select,insert,table):

        daly_aurora_to_redshift().created(select,insert)
        daly_aurora_to_redshift().updated(select,insert,table)

        return 'foi'



if __name__ == "__main__":

    selectQuery = \
        """
            SELECT * 
            from poli.messages_count 
            where date_occur  = '2022-07-13'
        """

    print(all_aurora_to_redshift.migration(selectQuery, None, None, None))    
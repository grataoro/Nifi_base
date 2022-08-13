try:
    import os
    import sys
    import json
    from datetime import datetime,timedelta

    dir_path = os.path.dirname(os.path.realpath(__file__))
    path = os.path.normpath(dir_path + '/../../..') 
    sys.path.append(path)

    from libs.pgsql import pgsql_class as pg

    path = os.path.normpath(dir_path + '/..') 
    sys.path.append(path)

    from pipe_lib import piperun, empresas

    dir_name = os.path.basename(__file__)

    day_1 = (datetime.now() + timedelta(days=-1,hours=-3)).strftime('%Y-%m-%d')
    url = "https://api.pipe.run/v1/companies?updated_at_start="+day_1+" 00:00:00&show=200&page={}"

    data    = piperun().get(url)
    records = empresas.records(data)
    emp_ids = piperun.ids(records)

    day = (datetime.now() + timedelta(days=-2,hours=-3)).strftime('%Y-%m-%d') + ' 23:59:59'
    pg("polichat").exec_pgsql("delete from piperun.companies where id in {}".format(emp_ids))
    pg("polichat").to_pgsql(records,'piperun.companies')


    end_time   = (datetime.now() + timedelta(hours=-3)).strftime(format= "%Y-%m-%d %H:%M:%S")

    print(json.dumps({"status":1, "response":"Success","origin":dir_name, "end_time":end_time}))

except Exception as e:

    end_time   = (datetime.now() + timedelta(hours=-3)).strftime(format= "%Y-%m-%d %H:%M:%S")
    print(json.dumps({"status":0, "response": str(e), "origin":dir_name,"end_time":end_time}))

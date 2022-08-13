import json
try:
    import os
    import sys
    from datetime import datetime, timedelta

    dir_path = os.path.dirname(os.path.realpath(__file__))
    path = os.path.normpath(dir_path + '/../../..') 
    sys.path.append(path)

    from libs.pgsql import pgsql_class as pg

    path = os.path.normpath(dir_path + '/..') 
    sys.path.append(path)

    from pipe_lib import piperun, atividades

    dir_name = os.path.basename(__file__)

    day_1 = (datetime.now() + timedelta(days=-1,hours=-3)).strftime('%Y-%m-%d')
    url = "https://api.pipe.run/v1/activities?created_at_start="+day_1+"&with=pipeline,stage,involved&show=200&page={}"
   
    data = piperun().get(url)
    records = atividades.records(data)

    day = (datetime.now() + timedelta(days=-2,hours=-3)).strftime('%Y-%m-%d') + ' 23:59:59'
    pg("polichat").exec_pgsql("delete from piperun.activities where created_at >'{}'".format(day))
    pg("polichat").to_pgsql(records,'piperun.activities (id, deal_id, activity_type_id, owner_id, involved_id, pipeline_id, stage_id, status_id, created_at, start_at, end_at, updated_at)')

    end_time   = (datetime.now() + timedelta(hours=-3)).strftime(format= "%Y-%m-%d %H:%M:%S")

    print(json.dumps({"status":1, "response":"Success","origin":dir_name, "end_time":end_time}))

except Exception as e:

    end_time   = (datetime.now() + timedelta(hours=-3)).strftime(format= "%Y-%m-%d %H:%M:%S")
    print(json.dumps({"status":0, "response": str(e), "origin":dir_name,"end_time":end_time}))

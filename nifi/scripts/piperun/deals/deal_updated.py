try:
    import os
    import sys
    import json
    import traceback
    from datetime import datetime,timedelta

    dir_path = os.path.dirname(os.path.realpath(__file__))
    path = os.path.normpath(dir_path + '/../../..') 
    sys.path.append(path)

    from libs.pgsql import pgsql_class as pg

    path = os.path.normpath(dir_path + '/..') 
    sys.path.append(path)

    from pipe_lib import piperun, oportunidades 

    dir_name = os.path.basename(__file__)

    day_1 = (datetime.now() + timedelta(days=-1,hours=-3)).strftime('%Y-%m-%d')

    url_opt = "https://api.pipe.run/v1/deals?updated_at_start="+day_1+" 00:00:00&with=users&show=200&page={}"

    opts    = piperun().get(url_opt)
    records = oportunidades.records(opts)
    opt_ids = piperun.ids(records)
  
    pg("polichat").exec_pgsql("delete from piperun.deals where id in {}".format(opt_ids))
    pg("polichat").to_pgsql(records,'piperun.deals (id, company_id, pipeline_id, stage_id, origin_id, owner_id, user_id, lost_reason_id, title, status_id, situation, mrr, value, temparatura, created_at, closed_at, updated_at)')
    
    end_time   = (datetime.now() + timedelta(hours=-3)).strftime(format= "%Y-%m-%d %H:%M:%S")

    print(json.dumps({"status":1, "response":"Success","origin":dir_name, "end_time":end_time}))

except:
    end_time   = (datetime.now() + timedelta(hours=-3)).strftime(format= "%Y-%m-%d %H:%M:%S")
    print(json.dumps({"status":0, "response": str(traceback.format_exc()), "origin":dir_name,"end_time":end_time}))

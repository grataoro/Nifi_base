try:
    import os
    import json
    import sys 
    import time
    from datetime import datetime
    from pipe_lib import pipe 
    from analytcs_lib import analy as ana

    dir_name = os.path.basename(__file__)

    inn = sys.stdin.read()

    webhook_data = json.loads(inn)

    time.sleep(420)

    opt = pipe.from_opt(webhook_data)

    if opt['cliente_id']:

        user_atv = ana.userActivity(opt['cliente_id'],opt['created_at'])

        dataFields =  ana.getDataFields(user_atv,webhook_data['origin']['id'])

        pipe.to_pipe(webhook_data['id'],dataFields)

        end_time   = datetime.now().strftime(format= "%Y-%m-%d %H:%M:%S")

        print(json.dumps({"status":1, "response":"Success","origin":dir_name, "end_time":end_time}))

except Exception as e:

    end_time   = datetime.now().strftime(format= "%Y-%m-%d %H:%M:%S")
    print(json.dumps({"status":0, "response": str(e), "origin":dir_name,"end_time":end_time}))

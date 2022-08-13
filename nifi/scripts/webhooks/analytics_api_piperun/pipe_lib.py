from requests import request
import json 


class pipe:
    def from_opt(data):    
        
        for form in data['forms']:
            if form['id'] == 13835:
                forms = form
                break

        for field in forms['fields']:
            if field['id'] == 184862:
                fields = field
                break

        return {    
        'id_opt'     : data['id'],
        'created_at' : data['created_at'][:10],
        'cliente_id' : fields['valor']
        }


    def to_pipe(id,dataFields):
        url = 'https://api.pipe.run/v1/deals/{}'.format(id)

        # payloads = json.dumps({"value": 'teste'})
        payloads = json.dumps({
        "custom_fields": [
            {
            "id": "185252", 
                    "value": dataFields['lastChannelGrouping']
                },
                {
            "id": "204167", 
                    "value": dataFields['lastSource']
                },
                {
            "id": "204168", 
                    "value": dataFields['lastMedium']
                },
                {
            "id": "189738", 
                    "value": dataFields['firstChannelGrouping']
                },
                {
            "id": "166984", 
                    "value": dataFields['firstPageView']
                },
                {
            "id": "204165", 
                    "value": dataFields['firstSource']
                },
                {
            "id": "204166", 
                    "value": dataFields['firstMedium']
                },
                {
            "id": "185257", 
                    "value": dataFields['isFirstVisit']
                },
                {
                    "id": "189736", 
                    "value": dataFields['countPageviewsBeforeConversion']
                }
            ]
        })


        headers = {
        'Content-Type': 'application/json',
        'token': '4586a7192ae763c5a3fbfb75f5b0511c'
        }


        response = request("PUT",url,headers=headers,data=payloads).json()
        return response
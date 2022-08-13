import os
import sys 
import json
from requests import request

dir_path = os.path.dirname(os.path.realpath(__file__))
path = os.path.normpath(dir_path + '/../..')
sys.path.append(path)

path = r'{}'.format(os.path.normpath(path + '/Auth/env.json'))
with open(path, 'r', encoding='utf8') as f:
        nectarToken = json.load(f)['nectar']['token']


class nectraApi:

    def get(url):

        headers = {
                'Content-Type' : 'application/json',
                'Access-Token' : nectarToken
                }   

        response = request("GET",url,headers=headers)
        
        if response.status_code == 200:
            return response.json()
        else: 
            pass



if __name__ == "__main__":

    url = "http://app.nectarcrm.com.br/crm/api/1/contatos/?displayLength=1"

    print(nectraApi.get(url))        



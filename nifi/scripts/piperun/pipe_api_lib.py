import os
import sys
import json

from requests import request
from unidecode import unidecode


dir_path = os.path.dirname(os.path.realpath(__file__))
path = os.path.normpath(dir_path + '/../..')
sys.path.append(path)

path = r'{}'.format(os.path.normpath(path + '/Auth/env.json'))
with open(path, 'r', encoding='utf8') as f:
        auth = json.load(f)



class pipeApi:
    
    
    headers = {
    'Content-Type': 'application/json',
    'token': auth['piperun'][0]['token']
    }


    def get(self, pipeUrl : str, date : str = None) -> list:

        if date:
            url = pipeUrl.format(date,1)

        else:
            url = pipeUrl.format(1)    


        jsonFromPipe = request("GET", url, headers=self.headers).json()
        data = jsonFromPipe['data']

        if 'meta' in jsonFromPipe:
            if jsonFromPipe['meta']['links']:
                nextPage = jsonFromPipe['meta']['links']['next']

                while 'next' in jsonFromPipe['meta']['links'].keys():
                    jsonFromPipe = request("GET", nextPage, headers=self.headers).json()
                    data = data + jsonFromPipe['data']

                    if 'next' in jsonFromPipe['meta']['links'].keys():
                        nextPage = jsonFromPipe['meta']['links']['next']

        return data
 

    def ids(records : list) -> tuple:
        lista : list = []
        for record in records:
            lista.append(record[0])
        return tuple(lista)   


    
    def str_validation(string : str, lenght : int) -> str:
        if string:
            return unidecode(string[:lenght])
        else:
            return string



if __name__ == "__main__":


    from datetime import datetime, timedelta
    day_1 = (datetime.now() + timedelta(days=-1,hours=-3)).strftime('%Y-%m-%d')

    url_opt = "https://api.pipe.run/v1/deals/16542385"
    
    print(pipeApi().get(url_opt))                
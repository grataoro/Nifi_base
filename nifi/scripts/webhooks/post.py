from requests import request 

url = "http://localhost:8889/teste"
#url = 'https://webhook-nifi.prod.cloud.polichat.com.br/teste'


with open('j.json','r') as j:
    data = j.read()


response = request("POST",url,data = data)
print('foi')
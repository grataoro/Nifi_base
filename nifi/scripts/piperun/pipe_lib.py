import os
import sys
import json
import requests
import numpy as np
import pandas as pd
from unidecode import unidecode
from datetime import datetime, timedelta


# acessa o diretorio das bibliotecas 
dir_path = os.path.dirname(os.path.realpath(__file__))
path = os.path.normpath(dir_path + '/../..')
sys.path.append(path)

import libs.logs_lib as log
from libs.pgsql import pgsql_class as pg

# acessa os diretorios das credenciais 
path = r'{}'.format(os.path.normpath(path + '/Auth/env.json'))
with open(path, 'r', encoding='utf8') as f:
        auth = json.load(f)


# classes con funções utilizadas em mais de um script 
class piperun:
    
    def __init__(self):
        self.headers = {
        'Content-Type': 'application/json',
        'token': auth['piperun'][0]['token']
        }

    # Entrada:
    #   url do piperun com o parametro &page={}
    # Retorno:
    #   uma lista de dicionário com os dados lidos de um json 
    # Função:
    #   faz uma paginação e retorna uma lista de dados 
    def get(self,url):
        response =requests.request("GET", url.format(1), headers=self.headers).json()
        data = response['data']

        for i in range(1,response['meta']['total_pages']):
            response = requests.request("GET", url.format(i+1), headers=self.headers).json()
            data = data + response['data']

        return data

    # Entrada:
    #   url do piperun com um parametro de data (&closed_at_start=aaaa-mm-dd) e o paametro de paginação "&page={}"
    # Retorno:
    #   uma lista de dicionário com os dados lidos de um json 
    # Função:
    #   faz uma paginação e retorna uma lista de dados 
    def get_with_date(self,url,date):
        response = requests.request("GET", url.format(date,1), headers=self.headers).json()
        data = response['data']

        for i in range(1,response['meta']['total_pages']):
            response = requests.request("GET", url.format(date,i+1), headers=self.headers).json()
            data = data + response['data']

        return data    

    # Entrada:
    #   lista de tuplas
    # Retorno:
    #   lista com os primeiros termos de cada elemeto da lista de entrada 
    def ids(records):
        lista = []
        for i in records:
            lista.append(i[0])
        return tuple(lista)   


    # Entrada:
    #   uma string e um integer
    # Retorno: 
    #   Uma string sem emojs e com o o mesmo nuemro de termos do integer de entrada
    def str_vlid(string,lenght):
        if string:
            return unidecode(string[:lenght])
        else:
            return string
     


class oportunidades:
    import re

    # Entrada:
    #   quarquer string
    # Retorno:
    #   steing 
    # Função:
    #   retirar emojs e passar para maiusculo 
    def validacao(text):
        comp = oportunidades.re.compile(r"[^ a-zA-Z0-9@\-+=/()[\]*:!$%&.]")
        text = unidecode(text)
        return comp.sub(r'',text).strip() 

    # Entrada:
    #   lista de dicionarios vindo das funções get ou get_with_date
    # Retorno:
    #   Uma lista de tuplas no formato aceito pelo banco 
    # Função:
    #   filtrar e tratar os dados 
    def records(opts):
        lista = []
        for opt in opts:

            if opt['title'] != None:
                titulo =oportunidades.validacao(opt['title'])
                titulo = (titulo[:195] + '...') if len(titulo) > 200 else titulo
            else:
                titulo = None 



            if opt['deleted'] == 1:
                situation = 1
            elif  opt['freezed'] == 1:
                situation = 2
            else:
                situation = 0       

            if opt['users']:
                id_user = opt['users'][0]['id']
            else:
                id_user = None    


            dic = {

                'id'             : opt['id'],
                'id_comapny'     : opt['company_id'],
                'id_pipeline'    : opt['pipeline_id'],
                'id_stage'       : opt['stage_id'],
                'id_origin'      : opt['origin_id'], 
                'id_owner'       : opt['owner_id'],
                'id_user'        : id_user,
                'id_lost_reason' : opt['lost_reason_id'],
                'title'          : titulo,
                'status'         : opt['status'],
                'situation'      : situation,
                'value_mrr'      : opt['value_mrr'],
                'value'          : opt['value'],
                'temperature'    : opt['temperature'],
                'created_at'     : opt['created_at'],
                'closed_at'      : opt['closed_at'],
                'updated_at'     : opt['updated_at']
            }

            lista.append(dic)

        df_opt = pd.DataFrame(lista)
        df_opt.replace({np.nan: None},inplace=True)

        return df_opt.to_records(index=False).tolist()


class atividades:

    # Entrada:
    #   lista de dicionarios vindo das funções get ou get_with_date
    # Retorno:
    #   Uma lista de tuplas no formato aceito pelo banco 
    # Função:
    #   filtrar e tratar os dados
    def records(atvs):
        lista = []
        for atv in  atvs:

            if 'pipeline' in atv:
                pipeline_id = atv['pipeline']['id']
            else:    
                pipeline_id = None

            if 'stage' in atv:
                stage_id = atv['stage']['id']
            else:
                stage_id = None    

            if atv['involved']:
                involved = atv['involved'][0]['id']
            else:
                involved = None


            dic = {
                'id'               : atv['id'],
                'id_deal'          : atv['deal_id'],
                'id_activity_type' : atv['activity_type_id'],
                'id_owner'         : atv['owner_id'],
                'involved'         : involved,
                'id_pipeline'      : pipeline_id ,
                'id_stage'         : stage_id,
                'status'           : atv['status'],
                'created_at'       : atv['created_at'],
                'start_at'         : atv['start_at'],
                'end_at'           : atv['delivery_date'],
                'updated_at'       : atv['updated_at']
            }

            lista.append(dic)
        
        df_opt = pd.DataFrame(lista)
        df_opt.replace({np.nan: None},inplace=True)

        return  df_opt.to_records(index=False).tolist()


class empresas:

    # Entrada:
    #   lista de dicionarios vindo das funções get ou get_with_date
    # Retorno:
    #   Uma lista de tuplas no formato aceito pelo banco 
    # Função:
    #   filtrar e tratar os dados
    def records(emps):

        lista = []
        for emp in emps:           

            dic = {
                'id'             : emp['id'],
                'id_owner'       : emp['owner_id'],
                'id_manager'     : emp['manager_id'],
                'id_poli'        : emp['external_code'],
                'id_cnae'        : emp['cnae_id'],
                'id_city'        : emp['city_id'],
                'email_nf'       : piperun.str_vlid(emp['email_nf'],250),
                'situation'      : emp['company_situation'],
                'cnpj'           : emp['cnpj'],
                'district'       : piperun.str_vlid(emp['district'],250),
                'social_capital' : emp['social_capital'],
                'cep'            : emp['cep'],
                'name'           : piperun.str_vlid(emp['name'],250),
                'company_name'   : piperun.str_vlid(emp['company_name'],250),
                'website'        : piperun.str_vlid(emp['website'],250),
                'address'        : piperun.str_vlid(emp['address'],250),
                'number'         : emp['address_number'],
                'size'           : emp['size'],
                'created_at'     : emp['created_at'],
                'updated_at'     : emp['updated_at']
            }

            lista.append(dic)     

        df_opt = pd.DataFrame(lista)
        df_opt.replace({np.nan: None},inplace=True)

        return  df_opt.to_records(index=False).tolist()  


class persons:

    # Entrada:
    #   lista de dicionarios vindo das funções get ou get_with_date
    # Retorno:
    #   Uma lista de tuplas no formato aceito pelo banco 
    # Função:
    #   filtrar e tratar os dados
    def records(pers):

        lista = []
        for per in pers:

            dic = {
                'id'             : per['id'],
                'company_id'     : per['company_id'],
                'city_id'        : per['city_id'],
                'owner_id'       : per['owner_id' ],
                'manager_id'     : per['manager_id'],
                'name'           : piperun.str_vlid(per['name'],250),
                'created_at'     : per['created_at'],
                'updated_at'     : per['updated_at']                
            }

            lista.append(dic)     

        df_opt = pd.DataFrame(lista)
        df_opt.replace({np.nan: None},inplace=True)

        return  df_opt.to_records(index=False).tolist()  


class customFields:

    # Entrada:
    #   lista de dicionarios vindo das funções get ou get_with_date
    # Retorno:
    #   Uma lista de tuplas no formato aceito pelo banco 
    # Função:
    #   filtrar e tratar os dados
    def records(opts):
        ids   = []
        lista = []
        for opt in opts:

            opt_id = opt['id']
            customfiels = opt['customFields']
            if customfiels:
                for customfiel in customfiels:

                    dic = {
                        'opt_id' : opt_id,
                        'csf_id' : customfiel['id'],
                        'type'   : customfiel['type'],
                        'value'  : piperun.str_vlid(str(customfiel['value']),999)
                    }

                    lista.append(dic)
            ids.append(opt_id)

        if lista:    
            
            df_opt = pd.DataFrame(lista)
            df_opt.replace({np.nan: None},inplace=True)

            return {"lista":df_opt.to_records(index=False).tolist(),"ids": tuple(ids)}  


    # Entrada:
    #   url do piperun, nome do diretorio, schema e nome da tabela e os ids que serão excluidos 
    # Retorno:
    #   um json com dados de logs 
    # Função:
    #   pegar os dados de campos customizados do piperun, via API, e salvar no redshift 
    def main(self,url,dir_name,table,id_column):
        try:
            day = (datetime.now() + timedelta(days=-1,hours=-3)).strftime('%Y-%m-%d')
            opts    = piperun().get_with_date(url,day)
            records = customFields.records(opts)
            if records:
                pg("polichat").exec_pgsql("delete from {} where {} in {}".format(table,id_column,records['ids']))
                pg("polichat").to_pgsql(records['lista'],table)

            return log.logs().susses(dir_name)

        except Exception as e:

            return log.logs().exception(dir_name,e)


class tabelas:

    # Entrada:
    #   url do piperun, nome dos campos do json, nome das tabelas e nome dos diretorios 
    # Retorno:
    #   Pega os dados de tabelas pequenas e salva no redshift 
    def main(url,coluns,table_name,dir_name):
        try:
            response = piperun().get(url) 
            df = pd.DataFrame(response)[coluns]
            records = df.to_records(index=False).tolist()

            pg("polichat").exec_pgsql("delete from piperun.{}".format(table_name))
            pg("polichat").to_pgsql(records, "piperun.{}".format(table_name))

            return log.logs().susses(dir_name)

        except Exception as e:
        
            return log.logs().exception(dir_name,e)

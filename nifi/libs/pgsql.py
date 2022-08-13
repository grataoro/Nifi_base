import os
import json
import psycopg2


dir_path = os.path.dirname(os.path.realpath(__file__))
path = os.path.normpath(dir_path + '/..')
path = r'{}'.format(os.path.normpath(path + '/Auth/env.json'))

with open(path, 'r', encoding='utf8') as f:
        auth = json.load(f)

class pgsql_class:

    def __init__(self,db = None):
        self.con =  psycopg2.connect(
            database = auth['redshift'][0]['database'],
            host     = auth['redshift'][0]['host'],
            user     = auth['redshift'][0]['user'],
            password = auth['redshift'][0]['password'],
            port     = auth['redshift'][0]['port']
            )

        self.cursor = self.con.cursor()    

    # Entrada:
    #    select: Select personalizado para consulta no banco
    # Retorno:
    #    retorna os registros de acordo com o select
    def from_pgsql(self,select):

        self.cursor.execute(select)

        myresult = self.cursor.fetchall()

        self.cursor.close()
        self.con.close()

        return myresult


    # Entrada:
    #    records : Redisteos no formato de uma lista de tuplas que serão inseridos no banco
    #    table   : schema e tabela onde os dados serão inseridos, podemos tambem especificar quais colunas serão utilizadas
    #    n_lines : n linhas a ser inseridas por vez
    # Retorno:
    #    retorna uma mensagem indicando que os registros foram inseridos
    
    def to_pgsql(self,records,table,n_lines = None):


        records_list_template = ','.join(['%s'] * len(records))

        insert_query = 'insert into {} values {}'.format(table,records_list_template)


        if n_lines:
            for i in range(0,len(records),n_lines):
                rec = records[i:i+n_lines]
                self.cursor.execute(insert_query, rec)
                self.con.commit()

        else:
            self.cursor.execute(insert_query, records)
            self.con.commit()

        self.cursor.close()
        self.con.close()
        return 'foi'


    # Entrada:
    #    sql     : Sql personalizado para consulta no banco
    # Retorno:
    #    retorna uma mensagem indicando que a sql foi executado
    def exec_pgsql(self,sql):

        self.cursor.execute(sql)
        self.con.commit()
        self.cursor.close()
        self.con.close()
        return 'foi'

    
    def insert(self,records,table):
        records_list_template = ','.join(['%s'] * len(records))
        return 'insert into {} values {}'.format(table,records_list_template)    
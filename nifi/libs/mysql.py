import mysql.connector
import json
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
path = os.path.normpath(dir_path + '/..')
path = r'{}'.format(os.path.normpath(path + '/Auth/env.json'))

with open(path, 'r', encoding='utf8') as f:
        auth = json.load(f)

class mysql_class:
    #    ced   : Especifica as credenciais do arquivo Auth.config
    def __init__(self,db=None) -> None:
        self.mydb = mysql.connector.connect(
                    database = db,
                    host     = auth['mysql'][0]['host'],   
                    user     = auth['mysql'][0]['user'],        
                    password = auth['mysql'][0]['password'], 
                    port     = auth['mysql'][0]['port']
        )    
    # Entrada:
    #    select: Select personalizado para consulta no banco
    # Retorno:  
    #    retorna os registros de acordo com o select 
    def from_mysql(self,select) -> list:

        mycursor = self.mydb.cursor()

        mycursor.execute(select)

        myresult = mycursor.fetchall()
        return myresult


        # Entrada:
        #    records : Redisteos no formato de uma lista de tuplas que serão inseridos no banco  
        #    table   : schema e tabela onde os dados serão inseridos, podemos tambem especificar quais colunas serão utilizadas 
        #    n_lines : n linhas a ser inseridas por vez
        # Retorno:  
        #    retorna uma mensagem indicando que os registros foram inseridos
    def to_mysql(self,records,table,n_lines = None):
       
        mycursor = self.mydb.cursor()   

        records_list_template = '({})'.format(','.join(['%s'] * len(records[0])))

        insert_query = 'insert into {} values {}'.format(table,records_list_template) 

        if n_lines:
            mycursor.executemany(insert_query, records)
            self.mydb.commit()

        else:
            for i in range(0,len(records),n_lines):
                rec = records[i:i+n_lines]
                mycursor.executemany(insert_query, rec)
                self.mydb.commit()

        
        mycursor.close()
        self.mydb.close()

        return 'foi'


    # Entrada:
    #    sql     : Sql personalizado para consulta no banco
    # Retorno:  
    #    retorna uma mensagem indicando que a sql foi executado
    def exec_mysql(self,sql):

        mycursor = self.mydb.cursor()
        mycursor.execute(sql) 
        self.mydb.commit()

        mycursor.close()
        self.mydb.close()
        return 'foi'  
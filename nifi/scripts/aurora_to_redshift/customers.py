import os

from full_insert_lib import fullInsert 


dirName = os.path.basename(__file__)

tableName = 'poli.customers'

select = \
"""
    SELECT id, customer_id, status, name, contact_name, contact_phone, adress_street, adress_number, adress_district, adress_postal_code, adress_city, adress_state, created_at, updated_at, reseller_id, cnpj 
    FROM customers
"""

tableNameWithSchema = "poli.customers (id, customer_id, status, name, contact_name, contact_phone, adress_street, adress_number, adress_district, adress_postal_code, adress_city, adress_state, created_at, updated_at, reseller_id, cnpj)"

migration = fullInsert(select).main(tableNameWithSchema,
                                    tableName,
                                    dirName)

print(migration)


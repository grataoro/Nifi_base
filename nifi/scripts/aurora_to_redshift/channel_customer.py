import os

from full_insert_lib import fullInsert 


dirName = os.path.basename(__file__)

tableName = 'poli.channel_customer'

select = \
"""
    SELECT id, customer_id, name, api, status, channel_id, created_at,updated_at, deleted_at,uid, phone 
    FROM  channel_customer
"""

tableNameWithSchema = "poli.channel_customer (id, customer_id, name, api, status, channel_id, created_at, updated_at, deleted_at, uid, phone)"

migration = fullInsert(select).main(tableNameWithSchema,
                                    tableName,
                                    dirName)

print(migration)


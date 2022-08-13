import os

from full_insert_lib import fullInsert 


dirName = os.path.basename(__file__)

tableName = 'poli.users'

select = \
"""
    SELECT id,name,status,customer_id,created_at,updated_at,deleted_at 
    FROM users
"""

tableNameWithSchema = "poli.users (id,name,status,customer_id,created_at,updated_at,deleted_at)"

migration = fullInsert(select).main(tableNameWithSchema,
                                    tableName,
                                    dirName)

print(migration)


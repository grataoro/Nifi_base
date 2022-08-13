import os

from full_insert_lib import fullInsert 


dirName = os.path.basename(__file__)

tableName = 'poli.settings'

select = \
"""
    SELECT id, customer_id, count_contacts, created_at, updated_at 
    FROM settings
"""

tableNameWithSchema = "poli.settings (id,customer_id,count_contacts,created_at,updated_at)"

migration = fullInsert(select).main(tableNameWithSchema,
                                    tableName,
                                    dirName)

print(migration)


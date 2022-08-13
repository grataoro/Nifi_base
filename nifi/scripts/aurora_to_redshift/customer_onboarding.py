import os

from full_insert_lib import fullInsert 


dirName = os.path.basename(__file__)

tableName = 'poli.customer_onboarding'

select = \
"""
    SELECT id,customer_id,type,status,created_at,updated_at 
    FROM customer_onboarding
"""

tableNameWithSchema = "poli.customer_onboarding (id,customer_id,type,status,created_at,updated_at)"

migration = fullInsert(select).main(tableNameWithSchema,
                                    tableName,
                                    dirName)

print(migration)


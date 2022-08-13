import os

from full_insert_lib import fullInsert 


dirName = os.path.basename(__file__)

tableName = 'poli.waba_authenticates'

select = \
"""
    SELECT id,uid,created_at,updated_at 
    FROM waba_authenticates
"""

tableNameWithSchema = "poli.waba_authenticates (id,uid,created_at,updated_at)"

migration = fullInsert(select).main(tableNameWithSchema,
                                    tableName,
                                    dirName)

print(migration)


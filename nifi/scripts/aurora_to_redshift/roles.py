import os

from full_insert_lib import fullInsert 


dirName = os.path.basename(__file__)

tableName = 'poli.roles'

select = \
"""
    SELECT id,name,label,obs,created_at,updated_at,deleted_at 
    FROM roles
"""

tableNameWithSchema = "poli.roles (id,name,label,obs,created_at,updated_at,deleted_at)"

migration = fullInsert(select).main(tableNameWithSchema,
                                    tableName,
                                    dirName)

print(migration)


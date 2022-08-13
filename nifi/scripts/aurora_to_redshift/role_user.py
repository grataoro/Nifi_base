import os

from full_insert_lib import fullInsert 


dirName = os.path.basename(__file__)


tableName = 'poli.role_user'

select = \
"""
    SELECT id, user_id, role_id, created_at, updated_at 
    FROM role_user
"""

tableNameWithSchema = "poli.role_user (id,user_id,role_id,created_at,updated_at)"

migration = fullInsert(select).main(tableNameWithSchema,
                                    tableName,
                                    dirName)

print(migration)


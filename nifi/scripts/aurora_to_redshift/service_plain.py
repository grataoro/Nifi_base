import os

from full_insert_lib import fullInsert 


dirName = os.path.basename(__file__)

tableName = 'poli.service_plain'

select = \
"""

    SELECT id, service_id, plain_id, interactions, channels, price, discount, created_at, updated_at
    FROM service_plain

"""

tableNameWithSchema = "poli.service_plain (id, service_id, plain_id, interactions, channels, price, discount, created_at, updated_at)"

migration = fullInsert(select).main(tableNameWithSchema,
                                    tableName,
                                    dirName)

print(migration)

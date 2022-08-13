import os

from full_insert_lib import fullInsert 


dirName = os.path.basename(__file__)


tableName = 'poli.customer_users'

select = \
"""
    SELECT customer_id,user_id 
    FROM customer_users
"""

tableNameWithSchema = "poli.customer_users (customer_id,user_id)"

migration = fullInsert(select).main(tableNameWithSchema,
                                    tableName,
                                    dirName)

print(migration)

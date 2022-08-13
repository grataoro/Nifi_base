import os

from full_insert_lib import fullInsert 


dirName = os.path.basename(__file__)

tableName = 'poli.shop_orders'

select = """
    SELECT id, customer_id, status, type, contact_id, created_at, updated_at, deleted_at 
    FROM shop_orders
"""

tableNameWithSchema = "poli.shop_orders (id, customer_id, status, type, contact_id, created_at, updated_at, deleted_at)"

migration = fullInsert(select).main(tableNameWithSchema,
                                    tableName,
                                    dirName)

print(migration)


import os

from full_insert_lib import fullInsert 


dirName = os.path.basename(__file__)

tableName = 'poli.shop_products'

select = \
"""
    SELECT id, customer_id, created_at, updated_at 
    FROM shop_products
"""

tableNameWithSchema = "poli.shop_products (id, customer_id, created_at, updated_at)"

migration = fullInsert(select).main(tableNameWithSchema,
                                    tableName,
                                    dirName)

print(migration)


import os

from full_insert_lib import fullInsert 


dirName = os.path.basename(__file__)

tableName = 'poli.shop_payment_integrators'

select = """
    SELECT id, customer_id, created_at, updated_at, deleted_at 
    FROM shop_payment_integrators
"""

tableNameWithSchema = "poli.shop_payment_integrators (id, customer_id, created_at, updated_at, deleted_at)"

migration = fullInsert(select).main(tableNameWithSchema,
                                    tableName,
                                    dirName)

print(migration)


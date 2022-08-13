import os

from full_insert_lib import fullInsert 


dirName = os.path.basename(__file__)

tableName = 'poli.plains'

select = \
"""
    SELECT id, customer_id, description, validate, amount, setup, discount, created_at, updated_at, paid
    FROM plains

"""

tableNameWithSchema = "poli.plains (id, customer_id, description, validate, amount, setup, discount, created_at, updated_at, paid)"

migration = fullInsert(select).main(tableNameWithSchema,
                                    tableName,
                                    dirName)

print(migration)

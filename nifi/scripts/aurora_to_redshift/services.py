import os

from full_insert_lib import fullInsert 


dirName = os.path.basename(__file__)

tableName = 'poli.services'

select = \
"""
    SELECT id, name, description, 'type', amount, 'free', status, superlogica_id, created_at, updated_at, quantity_contact_day
    FROM services

"""

tableNameWithSchema = "poli.services (id, name, description, type_, amount, free, status, superlogica_id, created_at, updated_at, quantity_contact_day)"

migration = fullInsert(select).main(tableNameWithSchema,
                                    tableName,
                                    dirName)

print(migration)

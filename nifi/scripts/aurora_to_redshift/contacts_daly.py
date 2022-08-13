import os

from migrations_lib import migrate


dirName = os.path.basename(__file__)

tableName = 'poli.contacts'

select = \
"""
    SELECT id, customer_id, department_id, name, channel_id, created_at, updated_at, deleted_at, phone, cpf
    FROM contacts
"""

tableNameWithSchema = "poli.contacts (id, customer_id, department_id, name, channel_id, created_at, updated_at, deleted_at, phone, cpf)"

migration = migrate(select).main(tableNameWithSchema,
                                    tableName,
                                    dirName,
                                    daly=True)

print(migration)


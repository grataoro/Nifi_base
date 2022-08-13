import os

from migrations_lib import migrate


dirName = os.path.basename(__file__)

tableName = 'poli.messages_count'

select = \
"""
    SELECT customer_id, channel_customer_id, contact_id, date_occur, created_at, updated_at, id 
    FROM messages_count
"""

tableNameWithSchema = "poli.messages_count (customer_id, channel_customer_id, contact_id, date_occur, created_at, updated_at, id )"

migration = migrate(select).main(tableNameWithSchema,
                                    tableName,
                                    dirName,
                                    daly=True)

print(migration)
